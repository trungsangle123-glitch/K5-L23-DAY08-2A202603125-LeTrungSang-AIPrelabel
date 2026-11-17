# Số đo review (det)

- Ảnh tính: 24 (batch,gold); box máy: 232; đối tượng sau duyệt: 226; ngưỡng accepted: IoU >= 0.9
- Đã **loại 17 đối tượng nằm quanh các bẫy** khỏi bảng này: lỗi nhân tạo không phản ánh chất lượng máy.

## 1. Bốn trạng thái (AI error profile)
| Trạng thái | Số | Tỉ lệ | Mẫu số |
|---|---|---|---|
| accepted (giữ nguyên) | 225 | 225/232 = 97.0% | 232 box máy |
| edited (sửa) | 0 | 0/232 = 0.0% | 232 box máy |
| deleted (xoá) | 7 | 7/232 = 3.0% | 232 box máy |
| added (vẽ thêm) | 1 | 1/226 = 0.4% | 226 đối tượng sau duyệt |

Trong số deleted + added, **1 trường hợp là đổi lớp** (máy gán sai lớp, box đúng chỗ): đó không phải máy bỏ sót. Số vật máy **sót thật** ≈ added − đổi lớp = 0.

### Theo lớp
| Lớp | accepted | edited | deleted | added |
|---|---|---|---|---|
| person | 109 | 0 | 1 | 0 |
| bicycle | 5 | 0 | 0 | 0 |
| motorbike | 67 | 0 | 2 | 0 |
| car | 27 | 0 | 0 | 0 |
| bus | 2 | 0 | 0 | 0 |
| truck | 1 | 0 | 1 | 0 |
| three_wheeler | 14 | 0 | 3 | 1 |

## 2. So với gold (nhãn gán tay từ đầu)
Ảnh gold: 4; đối tượng gold: 39 (mẫu số của recall)
| | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| Máy (pre-label) | 23 | 11 | 16 | 67.6% (KTC 95%: 51–81%) | 59.0% (KTC 95%: 43–73%) |

*Lạc quan: ngưỡng được chọn trên chính các ảnh gold này (in-sample), và chỉ có 4 ảnh. Đọc khoảng tin cậy, đừng đọc con số đơn.*


(Ảnh gold không nằm trong nhãn sau duyệt: không tính residual / new error. Đó là chủ ý: duyệt lại ảnh bạn vừa tự gán tay sẽ đo trí nhớ, không đo thiên kiến.)

## 3. Ảnh bẫy
- Bắt được 0/12 = 0.0% (KTC 95%: 0–24%) (ngưỡng đạt: 80%). Chỉ 12 bẫy nên khoảng tin cậy rất rộng: đọc cùng danh sách bẫy lọt, đừng kết luận chỉ từ %.
  - loose: 0/3
  - wrong_class: 0/3
  - extra: 0/3
  - missing: 0/3
  - lọt: img_009.jpg (loose), img_013.jpg (wrong_class), img_006.jpg (wrong_class), img_004.jpg (wrong_class), img_018.jpg (extra), img_031.jpg (loose), img_028.jpg (missing), img_023.jpg (extra), img_022.jpg (loose), img_025.jpg (extra), img_005.jpg (missing), img_024.jpg (missing)

## Gợi ý đọc số
- `deleted` cao → ngưỡng thấp hoặc ánh xạ nhãn sai; `added` cao → máy bỏ sót (xem lớp nào);
- `accepted` thấp (< 50%) → sửa mỗi box lâu hơn vẽ mới: đổi model/ngưỡng hoặc vẽ tay;
- bắt bẫy < 80% → duyệt lại lô, siết checklist (quét ảnh TRƯỚC khi nhìn nhãn máy).
