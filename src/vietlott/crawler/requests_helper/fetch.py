"""
fetch data utilities
"""

import re
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from io import StringIO
from typing import Callable, List, Optional, Tuple

import pandas as pd
import requests
from loguru import logger

from vietlott.crawler.requests_helper.config import TIMEOUT

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0"

# Timeout khi goi cac trang cung cap danh sach proxy
SOURCE_TIMEOUT = 25

# Sang loc proxy chet: bat tay TCP, chay song song
ALIVE_TIMEOUT = 3
SCREEN_WORKERS = 40

# Vietlott chan IP datacenter nuoc ngoai (IP cua GitHub Actions nam trong so do),
# nen uu tien proxy VN; proxy nuoc khac chi la phuong an cuoi.
PREFERRED_COUNTRY = "VN"

# Moi proxy chet ton toi TIMEOUT giay. Danh sach co ~300 proxy, neu thu het
# thi mot lan crawl co the keo dai hang gio -> bat buoc phai gioi han.
MAX_PROXIES_TO_TRY = 30

# Nhan gia cho "khong dung proxy". Vong dau luon thu di thang mot lan de kiem
# chung gia dinh 'IP GitHub bi Vietlott chan' - gia dinh nay chua ai kiem lai.
DIRECT = "direct"

# Proxy free chet rat nhanh, pool VN thay doi tung phut -> neu vong dau that bai
# thi lay lai danh sach moi roi thu them mot vong nua.
PROXY_ATTEMPTS = 3

# Lay lai danh sach ngay lap tuc thuong tra ve dung ban cu; cho mot chut de
# free-proxy-list.net kip cap nhat (pool VN co luc tut tu 7 xuong 1 trong 1 gio).
PROXY_RETRY_SLEEP = 10

# Proxy chet thuong chet ngay o buoc connect -> tach timeout connect cho ngan,
# giu timeout doc du dai cho proxy cham nhung song.
CONNECT_TIMEOUT = 6

# Chan tren thoi gian cho MOT task. Khong co cai nay thi truong hop xau nhat la
# PROXY_ATTEMPTS x MAX_PROXIES_TO_TRY x TIMEOUT = hang chuc phut cho moi task.
TASK_TIME_BUDGET = 120

bad_proxies = []
lock = threading.Lock()

# Task lay du lieu that bai. KHONG raise ngay giua chung vi se mat luon phan
# du lieu cac task khac da lay duoc; thay vao do ghi nhan lai, de crawl()
# ghi file xong roi moi bao loi.
failed_tasks = []

# get_proxies() duoc goi nhieu lan trong mot lan chay -> cache lai de khong
# spam free-proxy-list.net va de thu tu proxy on dinh giua cac task.
_proxies_cache: Optional[List[str]] = None
_proxies_cache_lock = threading.Lock()


def get_vietlott_cookie() -> Tuple[str, dict]:
    res = requests.get("https://vietlott.vn/ajaxpro/")
    match = re.search(r'document.cookie="(.*?)"', res.text)
    if match is None:
        raise ValueError(f"cookie is None, text={res.text}")
    cookie = match.group(1)
    cookies = {cookie.split("=")[0]: cookie.split("=")[1]}
    return cookie, cookies


def _parse_host_port(raw: str):
    raw = str(raw).strip()
    if ":" not in raw:
        return None
    host, port = raw.rsplit(":", 1)
    host = host.strip()
    try:
        port = str(int(float(port.strip())))
    except (ValueError, TypeError):
        return None
    if not host:
        return None
    return host, port


def _scheme_for(protocol: str) -> str:
    protocol = str(protocol).strip().upper()
    if protocol.startswith("SOCKS"):
        return "socks5" if "5" in protocol else "socks4"
    return "http"


def _find_proxy_table(tables: List[pd.DataFrame]) -> pd.DataFrame:
    """
    free-proxy-list.net doi layout theo thoi gian: bang dau tien khong con la bang
    proxy day du, va 2 cot 'IP Address' / 'Port' da bi gop thanh mot cot 'IP:Port'.
    Vi vay tim bang theo TEN COT thay vi hardcode index [0] nhu truoc.
    """
    for table in tables:
        cols = set(table.columns)
        has_address = ({"IP Address", "Port"} <= cols) or ("IP:Port" in cols)
        if has_address and "Code" in cols:
            return table

    raise ValueError(
        f"khong tim thay bang proxy, cac bang doc duoc: {[list(t.columns) for t in tables]}"
    )


def _source_free_proxy_list() -> List[str]:
    resp = requests.get(
        "https://free-proxy-list.net/",
        timeout=SOURCE_TIMEOUT,
        headers={"User-Agent": USER_AGENT},
    )
    resp.raise_for_status()
    table = _find_proxy_table(pd.read_html(StringIO(resp.text)))
    table = table[table["Code"] == PREFERRED_COUNTRY]

    out = []
    for _, row in table.iterrows():
        raw = row["IP:Port"] if "IP:Port" in row.index else f"{row['IP Address']}:{row['Port']}"
        parsed = _parse_host_port(raw)
        if parsed:
            scheme = _scheme_for(row["Protocol"]) if "Protocol" in row.index else "http"
            out.append(f"{scheme}://{parsed[0]}:{parsed[1]}")
    return out


def _source_proxyscrape() -> List[str]:
    out = []
    for protocol in ("http", "socks4", "socks5"):
        resp = requests.get(
            "https://api.proxyscrape.com/v2/",
            params={
                "request": "displayproxies",
                "protocol": protocol,
                "timeout": 10000,
                "country": PREFERRED_COUNTRY,
            },
            timeout=SOURCE_TIMEOUT,
            headers={"User-Agent": USER_AGENT},
        )
        resp.raise_for_status()
        for line in resp.text.splitlines():
            parsed = _parse_host_port(line)
            if parsed:
                out.append(f"{_scheme_for(protocol)}://{parsed[0]}:{parsed[1]}")
    return out


def _source_geonode() -> List[str]:
    resp = requests.get(
        "https://proxylist.geonode.com/api/proxy-list",
        params={
            "limit": 500,
            "page": 1,
            "sort_by": "lastChecked",
            "sort_type": "desc",
            "country": PREFERRED_COUNTRY,
        },
        timeout=SOURCE_TIMEOUT,
        headers={"User-Agent": USER_AGENT},
    )
    resp.raise_for_status()
    out = []
    for row in resp.json().get("data", []):
        parsed = _parse_host_port(f"{row.get('ip')}:{row.get('port')}")
        if not parsed:
            continue
        protocols = row.get("protocols") or ["http"]
        out.append(f"{_scheme_for(protocols[0])}://{parsed[0]}:{parsed[1]}")
    return out


PROXY_SOURCES = {
    "free-proxy-list": _source_free_proxy_list,
    "proxyscrape": _source_proxyscrape,
    "geonode": _source_geonode,
}


def _is_alive(proxy_url: str) -> bool:
    """
    Loc nhanh proxy chet bang ket noi TCP tran (dung cho ca http lan socks).
    Proxy chet chiem phan lon danh sach, ma moi cai ton CONNECT_TIMEOUT giay
    neu de cho requests tu phat hien -> sang loc truoc, song song, re hon nhieu.
    """
    try:
        host, port = proxy_url.split("://", 1)[1].rsplit(":", 1)
        with socket.create_connection((host, int(port)), timeout=ALIVE_TIMEOUT):
            return True
    except Exception:
        return False


def get_proxies(force_refresh: bool = False) -> List[str]:
    """
    Gom proxy VN tu NHIEU nguon. Mot nguon chet khong lam hong ca danh sach -
    truoc day chi co free-proxy-list.net, no doi layout HTML la crawler chet im.

    Danh sach rong -> raise, vi khong co proxy nghia la khong request nao duoc gui,
    crawler se im lang tra ve 'No results' y het khi khong co ky quay moi.
    """
    global _proxies_cache

    with _proxies_cache_lock:
        if _proxies_cache is not None and not force_refresh:
            return _proxies_cache

        collected: List[str] = []
        for name, source_fn in PROXY_SOURCES.items():
            try:
                found = source_fn()
                logger.info(f"nguon proxy {name}: {len(found)} proxy {PREFERRED_COUNTRY}")
                collected.extend(found)
            except Exception as error:
                logger.error(f"nguon proxy {name} loi: {type(error).__name__}: {error}")

        # giu thu tu xuat hien, bo trung
        unique = list(dict.fromkeys(collected))
        if not unique:
            raise ValueError(f"tat ca {len(PROXY_SOURCES)} nguon proxy deu khong tra ve gi")

        with ThreadPoolExecutor(max_workers=SCREEN_WORKERS) as pool:
            alive_flags = list(pool.map(_is_alive, unique))
        alive = [proxy for proxy, ok in zip(unique, alive_flags) if ok]

        logger.info(f"proxy: {len(unique)} gom duoc -> {len(alive)} con song")

        # neu sang loc khong con gi thi van thu danh sach goc, con hon khong thu
        _proxies_cache = alive or unique
        return _proxies_cache


def fetch_wrapper(
    url: str,
    headers: Optional[dict],
    org_params: Optional[dict],
    org_body: dict,
    process_result_fn: Callable,
    cookies: dict,
):
    """
    return a fn to fetch data for a set of params and body
    """

    def fetch(tasks):
        """
        perform fetching on multiple requests
        replace: org_params, org_body
        :param tasks: list of dict(task_id, task_data{params, body})
        :return:
        """
        tasks_str = ",".join(str(t["task_id"]) for t in tasks)
        logger.debug(f"worker start, tasks_ids={tasks_str}")
        _headers = headers.copy()

        results = []
        for task in tasks:
            task_id, task_data = task["task_id"], task["task_data"]
            params = org_params.copy()
            body = org_body.copy()

            params.update(task_data["params"])
            body.update(task_data["body"])

            done = False
            deadline = time.monotonic() + TASK_TIME_BUDGET
            for attempt in range(PROXY_ATTEMPTS):
                if time.monotonic() > deadline:
                    logger.warning(f"task {task_id}: het {TASK_TIME_BUDGET}s ngan sach thoi gian")
                    break
                if attempt > 0:
                    time.sleep(PROXY_RETRY_SLEEP)

                def _candidates():
                    # Thu di thang TRUOC, va chi khi that bai moi dung toi danh sach
                    # proxy - gom + sang loc proxy ton ~20s, khong viec gi phai tra
                    # cai gia do neu IP cua runner van vao duoc Vietlott.
                    if attempt == 0 and DIRECT not in bad_proxies:
                        yield DIRECT
                    # using proxy to avoid ban github ip
                    # tu vong 2 tro di lay lai danh sach proxy moi thay vi dung cache
                    all_proxies = get_proxies(force_refresh=True) if attempt else get_proxies()
                    used = 0
                    for proxy_url in all_proxies:
                        if proxy_url in bad_proxies:
                            continue
                        yield proxy_url
                        used += 1
                        if used >= MAX_PROXIES_TO_TRY:
                            return

                tried = 0
                for str_proxy in _candidates():
                    tried += 1
                    if time.monotonic() > deadline:
                        logger.warning(f"task {task_id}: het ngan sach thoi gian giua vong proxy")
                        break
                    proxy = None if str_proxy == DIRECT else {"http": str_proxy, "https": str_proxy}

                    try:
                        res = requests.post(
                            url,
                            json=body,
                            params=params,
                            headers=_headers,
                            cookies=cookies,
                            timeout=(CONNECT_TIMEOUT, TIMEOUT),
                            proxies=proxy,
                        )

                        if not res.ok:
                            banned_message = "You are unable to access"
                            if banned_message in res.text:
                                if str_proxy == DIRECT:
                                    logger.warning(
                                        "KET NOI TRUC TIEP BI CHAN - dung proxy la dung, "
                                        "gia dinh ban dau chinh xac"
                                    )
                                logger.error(
                                    f"req failed, args={task_data}, code={res.status_code}, "
                                    f"proxy={str_proxy}, res='Banned IP!!!'"
                                )
                            else:
                                logger.error(
                                    f"req failed, args={task_data}, code={res.status_code}, "
                                    f"proxy={str_proxy}, res={res.text[:200]}"
                                )
                            add_to_bad_list(str_proxy)
                            continue

                        try:
                            result = process_result_fn(params, body, res.json(), task_data)
                            results.append(result)
                            if str_proxy == DIRECT:
                                logger.info(
                                    "KET NOI TRUC TIEP THANH CONG - IP cua runner KHONG bi chan, "
                                    "co the bo han tang proxy"
                                )
                            logger.debug(f"task {task_id}, proxy={str_proxy} done")
                            done = True
                            break  # break the proxy loop
                        except Exception as error:
                            logger.error(
                                f"{type(error).__name__}, args={task_data}, text={res.text[:200]}, "
                                f"headers={headers}, cookies={cookies}, body={body}, params={params}"
                            )
                            add_to_bad_list(str_proxy)

                    # handle exception on request
                    except Exception as error:
                        logger.debug(f"{type(error).__name__}, task {task_id}, proxy={str_proxy}")
                        add_to_bad_list(str_proxy)

                if done:
                    break

                logger.warning(
                    f"task {task_id}: thu het {tried} duong o lan {attempt + 1}/{PROXY_ATTEMPTS}"
                )

            if not done:
                # KHONG duoc im lang bo qua: neu bo qua, crawl.py se in 'No results'
                # y het nhu khi khong co ky quay moi -> job xanh ma du lieu thieu.
                logger.error(
                    f"task {task_id}: khong lay duoc du lieu sau {PROXY_ATTEMPTS} vong proxy, "
                    f"bad proxies={len(bad_proxies)}"
                )
                with lock:
                    failed_tasks.append(task_id)

        logger.debug(f"worker done, tasks={tasks_str}")
        return results

    return fetch


def add_to_bad_list(item):
    with lock:
        if item not in bad_proxies:
            bad_proxies.append(item)


def reset_failures():
    """Goi truoc moi lan crawl de xoa ket qua cua lan truoc."""
    with lock:
        failed_tasks.clear()


def get_failures() -> List:
    with lock:
        return list(failed_tasks)
