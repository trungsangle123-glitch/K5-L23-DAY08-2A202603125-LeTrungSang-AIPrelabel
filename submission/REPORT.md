# Báo cáo Day 08 — <<MSHV - Họ và tên>>

> Mọi con số kèm **mẫu số** và nguồn (file nào, dòng nào). Viết bằng lời của bạn.

## 1. Tour model: chọn gì cho lớp nào

- So sánh các model (dẫn `model_log.csv`): <<điểm mạnh, điểm yếu, ví dụ ảnh>>
- Lỗi nào **không sửa được bằng đổi ngưỡng**? Sửa bằng cách nào?
- Ví dụ box **điểm cao mà sai** hoặc **điểm thấp mà đúng** (ảnh nào): <<>>

## 2. AI error profile (từ `qc/review_stats.md`)

| Trạng thái | Số | Tỉ lệ | Mẫu số |
|---|---|---|---|
| accepted | <<>> | <<>> | <<>> |
| edited | <<>> | <<>> | <<>> |
| deleted | <<>> | <<>> | <<>> |
| added | <<>> | <<>> | <<>> |

- Lớp nào máy tệ nhất? Vì sao (dẫn ảnh)? <<>>
- So với gold: precision / recall của **máy** <<>>; (nếu làm phần nâng cao) residual <<>>, new error <<>>.

## 3. Thiên kiến tự động hóa và ảnh bẫy

- Bắt bẫy: <<.../12>>; loại nào lọt: <<>>; vì sao (tôi đã bỏ bước nào của checklist)? <<>>
- Accepted cao mà bắt bẫy thấp (hoặc ngược lại) nói gì về cách tôi duyệt? <<>>

## 4. Máy có đáng dùng không?

- Thời gian: gán tay <<... phút/ảnh>> vs duyệt <<... phút/ảnh>> (từ `time_log.csv`); thiên lệch (tôi gán gold trước nên đã quen ảnh): <<>>
- Kết luận: <<có / không / chỉ cho lớp nào>> — dựa trên <<số liệu>>
- **Ba quy tắc giảm thiên kiến của tôi** (mỗi quy tắc kiểm tra được):
  1. <<>>
  2. <<>>
  3. <<>>

## 5. Segmentation và CVAT trực tiếp

- Lỗi mask hay gặp (người lái, hàng hoá, lỗ thủng, bóng): <<>>; quy tắc tôi áp dụng: <<>>
- Cách AI trực tiếp tôi đã thử (B1 / B2 / B3): <<>>; kết quả: <<chạy được / không chạy được: lỗi gì, đã thử gì>>
- So với offline import: <<thời gian, độ chính xác, độ dễ dùng>>

## 6. Calibration và bài học

- Quyết định guideline quan trọng nhất (dẫn `CAL-xx`): <<>>
- Nhất quán gán lại mù: IoU <<>>, cùng lớp <<>> (mẫu số <<>>): ca lệch lớn nhất <<>> → <<guideline mơ hồ hay tôi bất cẩn?>>
- Sửa script / lỗi script đã gặp (nếu có): <<>>
- Một điều tôi sẽ làm khác lần sau: <<>>
