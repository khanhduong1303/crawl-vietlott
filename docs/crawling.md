# Vietlott chặn crawl như thế nào

> Ghi lại ngày 2026-11-14, sau đợt sửa CI. Nguồn: log GitHub Actions run #2580.

## Vấn đề

Vietlott **đứng sau Cloudflare**. Không phải Vietlott tự chặn IP, mà Cloudflare
chặn hộ bằng bot protection.

Khi GitHub Actions gọi thẳng `vietlott.vn`:

```
HTTP 403
<title>Just a moment...</title>
```

`Just a moment...` là trang JS challenge của Cloudflare: nó bắt trình duyệt chạy
JavaScript để chứng minh là người thật. `requests` của Python không chạy JS nên
không bao giờ qua được.

## Vì sao Cloudflare chặn GitHub mà không chặn proxy VN

Cloudflare chấm điểm tin cậy theo IP:

- IP GitHub Actions là **datacenter**, dùng chung bởi vô số bot → điểm xấu → challenge.
- Proxy VN là **IP dân cư**. Kiểm tra nhà mạng của chúng (dữ liệu geonode):

  ```
   30  Viettel Group          5  Vietnam Internet Network Information Center
   24  Viettel Corporation    4  Newass2011xDSLHN
   12  FPT Telecom Company    3  VIETELxdsl
  ```

  Toàn Viettel / FPT / VNPT, có cả tên ghi thẳng `xDSL`.

**Mấu chốt: không phải "IP Việt Nam" mới qua được, mà "IP dân cư" mới qua được.**
Đây là chỗ dễ nhầm nhất.

## Hướng crawl: cái nào khả thi

| Hướng | Được không | Ghi chú |
|---|---|---|
| **Proxy free VN** (đang dùng) | ✅ | Miễn phí. Gộp nhiều nguồn: ~260 gom được, ~25 sống. Chập chờn nhưng đủ dùng |
| **Self-hosted runner ở nhà** | ✅ Tốt nhất | IP dân cư VN, bỏ hẳn proxy. Đổi lại: máy phải thức 24/7, và GitHub khuyến cáo không dùng cho repo public |
| **Proxy residential trả phí** | ✅ | Ổn định nhất, tốn tiền. Phải là *residential*, không phải datacenter proxy |
| **VPS Việt Nam** | ❌ Nhiều khả năng hỏng | IP datacenter, đúng loại Cloudflare nghi ngờ. Ở VN cũng không cứu được |
| **Gọi thẳng từ GitHub Actions** | ❌ | Đã test, 403 |
| Giả header / đổi User-Agent | ❌ | Code đã làm rồi, không ăn thua. Cloudflare chặn theo IP chứ không theo header |

Nếu sau này cần nâng cấp: **self-hosted runner** → **proxy residential trả phí**.
Đừng thuê VPS VN vì tưởng "ở VN là qua được".

## Cách crawler đang làm

Xem [`fetch.py`](../src/vietlott/crawler/requests_helper/fetch.py).

1. Thử **đi thẳng** trước (rẻ, và tự ghi log kết quả vào CI).
2. Thất bại thì rơi xuống proxy: gộp 3 nguồn `free-proxy-list` + `proxyscrape` +
   `geonode`, chỉ lấy proxy VN.
3. Lọc proxy chết bằng bắt tay TCP song song trước khi dùng.
4. Mỗi task có ngân sách thời gian `TASK_TIME_BUDGET`, thử tối đa
   `MAX_PROXIES_TO_TRY` proxy, `PROXY_ATTEMPTS` vòng.

Dấu hiệu trang chặn nhận diện trong `BLOCK_MARKERS`: `Just a moment`,
`Attention Required`, `cf-browser-verification`, `Checking your browser`.

### Khi nào job báo đỏ

| Tình huống | Kết quả |
|---|---|
| Không có kỳ quay mới | 🟢 bình thường (crawl 8 lần/ngày, tuần quay 3 lần) |
| Lấy được dữ liệu, vài task hỏng | 🟢 + cảnh báo trong log |
| Về tay không **mà có task hỏng** | 🔴 đỏ |

Job đỏ là tín hiệu thật, đáng đi xem.

Đọc log của một run mà không cần `gh`: script local `ci-log.sh <run_id>` (không
nằm trong repo, đã gitignore vì là tiện ích riêng của máy), hoặc mở thẳng trang
run trên GitHub và tìm chữ `TRUC TIEP`.

## Độ chắc chắn

- 403 + trang Cloudflare: **bằng chứng trực tiếp** từ log CI.
- "IP dân cư nên được cho qua": **suy luận** từ việc proxy Viettel/FPT vào được
  còn IP GitHub thì không. Hợp lý nhưng không đọc được luật chặn thật của Cloudflare.
- "VPS VN nhiều khả năng hỏng": **chưa test**, chỉ suy ra từ điểm trên. Muốn chắc
  phải thuê thử.
