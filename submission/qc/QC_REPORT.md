# Báo cáo QC — <<MSHV - Họ và tên>>

> Thay mọi `<<...>>`. Lấy số từ `qc_report_auto.md`, `review_stats.md`, `self_check.md`. Mọi tỉ lệ **kèm mẫu số**.

## 1. Lô

| Mục | Giá trị |
|---|---|
| Tên lô | day08-street-24 (tập batch) |
| Số ảnh | 24 |
| Recipe pre-label | <<model + ngưỡng, dẫn recipe.md>> |
| Phiên bản guideline lúc gán | <<v1.0>> |
| Phiên bản guideline hiện tại | <<v1.1>> |

## 2. Mẫu QC

- Cỡ mẫu: <<n>> ảnh (<<m>> ảnh có `can_review` + <<k>> ảnh ngẫu nhiên, seed <<42>>).
- Cách chọn và vì sao mẫu nhỏ (24 ảnh, bài học): <<>>
- Người kiểm: <<tôi>>; ngày: <<YYYY-MM-DD>>. (Nếu bạn là người vừa duyệt: nói rõ đây là hạn chế, người kiểm lý tưởng là người khác.)

## 3. Số đo

| Cách đếm | Lỗi | Mẫu số | Tỉ lệ |
|---|---|---|---|
| Theo **đối tượng** | <<>> | <<đối tượng trong mẫu>> | <<>> % |
| Theo **ảnh** (ngưỡng Release ≤ 2%) | <<>> | <<ảnh trong mẫu>> | <<>> % |

| Chỉ số khác | Giá trị | Mẫu số | Ngưỡng | Đạt? |
|---|---|---|---|---|
| Bắt bẫy | <<>> | <<12 bẫy>> | ≥ 80% | <<>> |
| Gán lại mù: IoU TB | <<>> | <<cặp box>> | ≥ 0.85 | <<>> |
| Gán lại mù: cùng lớp | <<>> % | <<cặp box>> | ≥ 95% | <<>> |

## 4. Lỗi

Top 3 loại lỗi (trong: bỏ sót, thừa, sai lớp, sai vị trí/kích thước, sai thuộc tính, sai mask), mỗi loại một ảnh ví dụ:

| Hạng | Loại lỗi | Số lỗi | Ảnh ví dụ | Nguyên nhân gốc (máy / guideline mơ hồ / tôi) |
|---|---|---|---|---|
| 1 | <<>> | <<>> | <<img_0xx>> | <<>> |
| 2 | <<>> | <<>> | <<>> | <<>> |
| 3 | <<>> | <<>> | <<>> | <<>> |

Lỗi **lặp lại cùng một kiểu** không? <<có / không, kiểu nào>>

## 5. Calibration

- Số quyết định đã ghi: <<>> (`calibration_decisions.csv`); ba cái quan trọng nhất: <<ca → quyết định → phiên bản>>
- Quy tắc mới đã vào guideline: <<v1.1: ...>>
- Nguyên nhân bất đồng chính: <<guideline mơ hồ / chưa nắm quy tắc / máy>>

## 6. Script kiểm được gì, không kiểm được gì

- Script đã kiểm: <<tên lớp, box trong ảnh, đủ ảnh, ...>>
- Script **không** kiểm được, và tôi đã dùng mắt người ra sao: <<box ôm sát? cả tôi và máy cùng bỏ sót? tôi có thật sự theo checklist?>>
- Giới hạn thống kê của mẫu nhỏ: <<quy tắc 3/n: 0 lỗi trong n ảnh nghĩa là gì>>

## 7. Quyết định

**<<Release / Hold / Rework>>** — ngày <<YYYY-MM-DD>>.

Lý do (đi theo cây Hold → Rework → Release):
1. Guideline chưa rõ / dữ liệu hỏng? <<>>
2. > 2% ảnh lỗi, lỗi lặp lại, bắt bẫy < 80%, hoặc nhất quán dưới ngưỡng? <<>>
3. Kết luận: <<>>

Nếu **Rework / Hold**: việc cần làm tiếp: <<>>
