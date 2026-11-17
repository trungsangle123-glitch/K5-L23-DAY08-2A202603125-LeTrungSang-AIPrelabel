# Label contract — Phố châu Á — BỔ SUNG v1.1 — 2A202603125 - LeTrungSang

> Chỉ ghi phần **thay đổi so với v1.0**. Mỗi ca khó có ảnh ví dụ (`img_0xx`) và khớp một dòng trong `qc/calibration_decisions.csv`.

## 1. Câu hỏi mở đã chốt (từ mục 6 của v1.0)

| # | Câu hỏi | Quyết định | Ảnh ví dụ | `case_id` |
|---|---|---|---|---|
| 1 | Xe ba gác/tuk-tuk: `car`, `motorbike` hay `three_wheeler`? | `three_wheeler` cho mọi biến thể (tuk-tuk, cyclo, cargo tricycle). YOLO26 không có lớp này nên phải lấy từ YOLOE rồi merge ưu tiên. | img_004.jpg | CAL-01 |
| 2 | Người lái trên xe ba bánh gán lớp nào? | `person`, không gán theo phương tiện. | img_013.jpg | CAL-02, CAL-03 |
| 3 | Box rất nhỏ ở nền xa (cao < 20px) giữ lớp hay bỏ? | Chuyển `ignore_region`; không ép nhãn khi không đủ pixel để phân biệt. | img_027.jpg | CAL-04 |

## 2. Ca khó mới (từ lỗi của máy, bẫy lọt, box `can_review`)

| Ảnh | Tình huống | Máy làm gì (model nào) | Quyết định của bạn | Quy tắc mới (vào mục nào của v1.0) |
|---|---|---|---|---|
| img_004.jpg | Tuk-tuk bị gọi nhầm `motorbike` | YOLO26-n @640, cop 0.25 (`r05`), sai lớp; đổi ngưỡng không sửa được | Đổi `three_wheeler`; dùng YOLOE riêng cho lớp này | Mục 2 · định nghĩa lớp (CAL-01) |
| img_006.jpg | Người bị gọi nhầm `bicycle` | Bẫy `wrong_class` trong pre-label sau merge | Đổi `person`, tick `can_review` | Mục 2 · người lái (CAL-02) |
| img_013.jpg | Người trên xe ba bánh bị gọi `bicycle` | Bẫy `wrong_class`, cùng quy luật với img_006 | Đổi `person` | Mục 2 · người lái (CAL-03) |
| img_027.jpg | Box `car` cao 17.1px | `validate_labels.py` cảnh báo vật quá nhỏ | Chuyển `ignore_region` | Mục 2 · ngưỡng kích thước (CAL-04) |
| img_031.jpg | Box `person` để hở nền | Bẫy `loose`: box lệch khỏi vật | Kéo sát 4 cạnh về box gốc | Mục 4.2 · kiểm 4 cạnh (CAL-05) |
| img_009.jpg | Box chạm viền ảnh, cắt người | Bẫy `loose` + nằm sát mép trái | Kéo về vật, tick `can_review` | Mục 4.2 · box chạm viền (CAL-06) |

## 3. Lịch sử thay đổi

| Phiên bản | Thay đổi | Lý do (ca nào, `case_id`) |
|---|---|---|
| v1.0 | Bản giảng viên | — |
| v1.1 | Chốt 3 câu hỏi mở; thêm quy tắc `three_wheeler`, người lái = `person`, ngưỡng 20px → `ignore_region`, kiểm 4 cạnh và box chạm viền | CAL-01 … CAL-06 (từ lỗi máy + bẫy lọt trong `model_log.csv`, `traps_key.json`, `review_stats.json`) |
