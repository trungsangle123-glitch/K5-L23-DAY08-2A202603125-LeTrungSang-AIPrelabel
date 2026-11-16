# Chọn ngưỡng tin cậy theo lớp (Part 3, 15 phút)

**Một việc duy nhất:** tìm ngưỡng `conf` cho **từng lớp** để pre-label ít box thừa mà không bỏ sót thêm.

Không có ngưỡng hoàn hảo, chỉ có đánh đổi: ngưỡng **thấp** → nhiều box thừa (mất công xoá); ngưỡng **cao** → bỏ sót (lỗi lọt vào dataset, khó thấy).

## Làm gì

1. Gộp pre-label của 4 ảnh gold (ngưỡng thấp 0.10) rồi quét ngưỡng với **nhãn gán tay** của bạn làm chuẩn ([GUIDE.md](../GUIDE.md) Part 3):
   ```bash
   python scripts/merge_prelabels.py work/prelabel/yoloe_all/pre.coco.json work/prelabel/y26_all/pre.coco.json \
       --conf 0.1 --iou 0.6 --split gold --out work/prelabel/merged_gold/pre.coco.json
   python scripts/threshold_sweep.py --pred work/prelabel/merged_gold/pre.coco.json --gold submission/labels/gold_manual.json
   ```
2. Mở `submission/qc/threshold_sweep.md` (bảng ngưỡng gợi ý) và `threshold_sweep.png` (precision / recall theo ngưỡng).
3. Copy chuỗi `--thr "..."` in ra vào lệnh `merge_prelabels.py` ở Part 4, và ghi ngưỡng cùng lý do vào `REPORT.md` mục 1.

## Đọc kết quả

- **Ngưỡng gợi ý** = ngưỡng **cao nhất** mà recall của lớp đó còn ≥ 0.9. Nghĩa là ít box thừa nhất trong khi chưa bỏ sót thêm.
- Dòng ghi *"KHÔNG đạt recall 90%"*: không ngưỡng nào đạt mục tiêu; script lấy ngưỡng có F1 cao nhất. Hãy nói trong báo cáo vì sao (thường: model không biết lớp đó).
- Dòng ghi *"không có vật ... trong ảnh gold"*: không đo được; giữ ngưỡng mặc định.

## Hai giới hạn phải nói trong báo cáo

- **Chọn và chấm trên cùng dữ liệu:** bạn chọn ngưỡng trên gold rồi (ở Part 4) đo máy trên gold, nên precision / recall của máy trên gold là **lạc quan**. Muốn chặt hơn: pilot riêng ở [ADVANCED.md](ADVANCED.md) mục 3.
- **Mẫu nhỏ:** chỉ 4 ảnh gold. Lớp ít vật (xem cột `n_gold` trong `threshold_sweep.csv`) thì ngưỡng chỉ là ước lượng thô.
