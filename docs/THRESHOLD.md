# Chọn ngưỡng tin cậy theo lớp (Part 3)

**Một việc duy nhất:** tìm ngưỡng `conf` cho **từng lớp** để pre-label ít box thừa mà không bỏ sót thêm.

Không có ngưỡng hoàn hảo, chỉ có đánh đổi: ngưỡng **thấp** → nhiều box thừa (mất công xoá); ngưỡng **cao** → bỏ sót (lỗi lọt vào dataset, khó thấy).

## Làm gì

1. Duyệt pilot trong CVAT, export `submission/labels/pilot_reviewed.json` (xem [GUIDE.md](../GUIDE.md) Part 3).
2. Chạy:
   ```bash
   python scripts/threshold_sweep.py --pred work/prelabel/merged_pilot/pre.coco.json \
       --gold submission/labels/pilot_reviewed.json
   ```
3. Mở `submission/qc/threshold_sweep.md` (bảng ngưỡng gợi ý) và `threshold_sweep.png` (precision / recall theo ngưỡng).
4. Copy chuỗi `--thr "..."` in ra vào lệnh `merge_prelabels.py` ở Part 4, và ghi ngưỡng cùng lý do vào `submission/recipe.md`.

## Đọc kết quả

- **Ngưỡng gợi ý** = ngưỡng **cao nhất** mà recall của lớp đó còn ≥ 0.9. Nghĩa là ít box thừa nhất trong khi chưa bỏ sót thêm.
- Dòng ghi *"KHÔNG đạt recall 90%"*: không ngưỡng nào đạt mục tiêu; script lấy ngưỡng có F1 cao nhất. Hãy nói trong báo cáo vì sao (thường: model không biết lớp đó).
- Dòng ghi *"không có vật ... trong pilot"*: không đo được; giữ ngưỡng mặc định.

## Hai giới hạn phải nói trong báo cáo

- **Nhãn chuẩn pilot do máy dựng một nửa:** bạn sửa pre-label ngưỡng 0.10, nên vật có điểm dưới 0.10 mà bạn không tự vẽ thì vắng mặt. Recall thật thấp hơn recall đo được. Vì vậy ngưỡng quét bắt đầu từ 0.10.
- **Mẫu nhỏ:** pilot chỉ 6 ảnh. Lớp ít vật (xem cột `n_gold` trong `threshold_sweep.csv`) thì ngưỡng chỉ là ước lượng thô.
