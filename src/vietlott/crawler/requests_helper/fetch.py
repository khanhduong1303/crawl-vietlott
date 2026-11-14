"""
fetch data utilities
"""

import re
import threading
from io import StringIO
from typing import Callable, List, Optional, Tuple

import pandas as pd
import requests
from loguru import logger

from vietlott.crawler.requests_helper.config import TIMEOUT

PROXY_LIST_URL = "https://free-proxy-list.net/"

# Vietlott chan IP datacenter nuoc ngoai (IP cua GitHub Actions nam trong so do),
# nen uu tien proxy VN; proxy nuoc khac chi la phuong an cuoi.
PREFERRED_COUNTRY = "VN"

# Moi proxy chet ton toi TIMEOUT giay. Danh sach co ~300 proxy, neu thu het
# thi mot lan crawl co the keo dai hang gio -> bat buoc phai gioi han.
MAX_PROXIES_TO_TRY = 25

bad_proxies = []
lock = threading.Lock()

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
        f"khong tim thay bang proxy tren {PROXY_LIST_URL}, "
        f"cac bang doc duoc: {[list(t.columns) for t in tables]}"
    )


def _to_proxy_url(row: pd.Series) -> Optional[str]:
    """Chuyen mot dong cua bang proxy thanh URL co scheme, vd http://1.2.3.4:8080"""
    try:
        if "IP:Port" in row.index:
            raw = str(row["IP:Port"]).strip()
            if ":" not in raw:
                return None
            host, port = raw.rsplit(":", 1)
        else:
            host, port = str(row["IP Address"]).strip(), str(row["Port"]).strip()

        # pandas co the doc Port thanh float (8080.0)
        port = str(int(float(port)))
        host = host.strip()
        if not host or not port:
            return None

        protocol = str(row["Protocol"]).strip().upper() if "Protocol" in row.index else "HTTP"
        if protocol.startswith("SOCKS"):
            scheme = "socks5" if "5" in protocol else "socks4"
        else:
            scheme = "http"

        return f"{scheme}://{host}:{port}"
    except (ValueError, TypeError, KeyError):
        return None


def get_proxies(force_refresh: bool = False) -> List[str]:
    """
    Tra ve danh sach proxy URL, proxy VN xep truoc.

    Khac ban cu: KHONG nuot loi tra ve DataFrame rong nua. Danh sach proxy rong
    dong nghia voi viec khong request nao duoc gui di, crawler se im lang tra ve
    'No results' nhu the khong co ky quay moi -> phai bao loi that to.
    """
    global _proxies_cache

    with _proxies_cache_lock:
        if _proxies_cache is not None and not force_refresh:
            return _proxies_cache

        resp = requests.get(
            PROXY_LIST_URL,
            timeout=TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0"},
        )
        resp.raise_for_status()

        table = _find_proxy_table(pd.read_html(StringIO(resp.text)))

        preferred = table[table["Code"] == PREFERRED_COUNTRY]
        others = table[table["Code"] != PREFERRED_COUNTRY]

        urls: List[str] = []
        for _, row in pd.concat([preferred, others]).iterrows():
            url = _to_proxy_url(row)
            if url and url not in urls:
                urls.append(url)

        logger.info(
            f"proxy list: {len(preferred)} proxy {PREFERRED_COUNTRY} / {len(urls)} tong cong, "
            f"se thu toi da {MAX_PROXIES_TO_TRY} cai"
        )

        if not urls:
            raise ValueError(f"danh sach proxy rong tu {PROXY_LIST_URL}")

        _proxies_cache = urls
        return urls


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
        # using proxy to avoid ban github ip
        all_proxies = get_proxies()

        results = []
        for task in tasks:
            task_id, task_data = task["task_id"], task["task_data"]
            params = org_params.copy()
            body = org_body.copy()

            params.update(task_data["params"])
            body.update(task_data["body"])

            candidates = [p for p in all_proxies if p not in bad_proxies][:MAX_PROXIES_TO_TRY]
            if not candidates:
                logger.error(f"task {task_id}: khong con proxy nao kha dung (bad list={len(bad_proxies)})")
                continue

            done = False
            for str_proxy in candidates:
                proxy = {"http": str_proxy, "https": str_proxy}

                try:
                    res = requests.post(
                        url,
                        json=body,
                        params=params,
                        headers=_headers,
                        cookies=cookies,
                        timeout=TIMEOUT,
                        proxies=proxy,
                    )

                    if not res.ok:
                        banned_message = "You are unable to access"
                        if banned_message in res.text:
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

            if not done:
                logger.error(
                    f"task {task_id}: thu het {len(candidates)} proxy deu that bai"
                )

        logger.debug(f"worker done, tasks={tasks_str}")
        return results

    return fetch


def add_to_bad_list(item):
    with lock:
        if item not in bad_proxies:
            bad_proxies.append(item)
