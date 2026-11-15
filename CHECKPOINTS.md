# Checkpoints — Day 08

Bài cá nhân, dự kiến **6–8 giờ** (nên chia 3 buổi). Giờ trong bảng là mốc cho người làm nhanh, máy có GPU. Mốc tính từ lúc bắt đầu, là điểm **tự kiểm tra**, không phải hạn nộp. Deadline do giảng viên/coach thông báo.

| Mốc | Mục tiêu | Tự kiểm tra |
|---|---|---|
| 0:25 | **CP0** Cài đặt | `check_env.py` SẴN SÀNG; chạy được YOLO26 trên một ảnh; Project CVAT có 8 nhãn |
| 1:15 | **CP1** Gold | `gold_manual.json` qua `validate_labels`; chưa hề xem pre-label của 6 ảnh gold; có `time_log` |
| 2:45 | **CP2** Tour model | `model_log.csv` ≥ 6 dòng, ≥ 3 model, có nhận xét; đã chạy `--split all --conf 0.05` |
| 3:40 | **CP3** Pilot | `pilot_reviewed.json`; `threshold_sweep.md` có ngưỡng theo lớp |
| 3:50 | Nghỉ | |
| 5:00 | **CP4** Review | `batch_reviewed.json`; `review_stats.md` có bắt bẫy % và precision / recall của máy so với gold |
| 5:50 | **CP5** Segmentation | `seg_reviewed.json` có polygon; đã thử một cách AI trực tiếp trong CVAT |
| 7:00 | **CP6** Calibration + QC + nộp | `guideline_v1.1`, `QC_REPORT.md` có quyết định; `check_submission.py` sạch; đã nộp link |

## Chi tiết từng checkpoint

### CP1 · Cần hiểu
Vì sao gold phải gán **trước** khi thấy máy? Neo nhãn nghĩa là gì và nó làm sai số đo nào?

### CP2 · Cần hiểu
Vì sao YOLO26 gọi tuk-tuk là `car`? Open-vocabulary khác closed-set ở điểm nào, và chữ prompt ảnh hưởng thế nào?

### CP3 · Cần hiểu
Vì sao chọn ngưỡng **theo lớp**, bằng tập **pilot** chứ không bằng gold? "Điểm tin cậy 0.9" có phải "90% đúng" không?

### CP4 · Cần hiểu
`accepted` cao nhưng bắt bẫy thấp nghĩa là gì? Lỗi nào của máy **không hiện** trên điểm số (bỏ sót)? Vì sao precision / recall của máy đo trên **gold** đáng tin hơn trên chính nhãn bạn vừa duyệt?

### CP5 · Cần hiểu
"Một click, ba mask": ai quyết mask gồm gì (người lái? hàng hoá?)? Vì sao mask đúng không cứu được nhãn lớp sai?

### CP6 · Cần hiểu
Tầng calibration nào sửa **guideline**, tầng nào sửa **người**? Vì sao 0 lỗi trong 10 ảnh mẫu chưa chứng minh "dưới 2%"?

Chi tiết lệnh xem [GUIDE.md](GUIDE.md). Nếu CVAT chậm, mỗi người có thể cài CVAT local (Docker) hoặc dùng tài khoản cvat.ai riêng từ trước buổi học.
