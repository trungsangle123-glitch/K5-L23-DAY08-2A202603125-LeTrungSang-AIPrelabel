# Thư mục nộp bài

Xem cấu trúc bắt buộc ở [../SUBMISSION.md](../SUBMISSION.md). Các file bạn **tự điền** (khuôn có sẵn ở đây):

| File | Điền gì | Ví dụ một dòng |
|---|---|---|
| `model_log.csv` | mỗi lần chạy `prelabel.py` một dòng; copy cột có sẵn từ `work/runs.csv`, tự viết 3 cột nhận xét | `r03,2C,yoloe,"--prompts 'tuk-tuk=three_wheeler' --conf 0.25",pilot,9,0.3,"tìm 4/5 tuk-tuk ở img_002","bỏ sót xích lô img_011; box lỏng rộng hơn xe ~10%","dùng cho three_wheeler, thêm prompt 'cyclo'"` |
| `time_log.csv` | thời gian **thật** từng bước | `gold_manual,6,38,"gán tay 6 ảnh, 101 box"` |
| `recipe.md` | recipe pre-label cuối (khuôn trong file) | |
| `REPORT.md` | báo cáo chính (6 mục, khuôn trong file) | |
| `individual_note.md` | ghi chú cá nhân + công cụ AI đã dùng | |
| `qc/calibration_decisions.csv` | mỗi quyết định calibration **một dòng** (xem docs/CALIBRATION_QC.md) | `CAL-01,img_013|img_004,loi_may,"YOLO26 gọi tuk-tuk là car",gán lại thành three_wheeler,"mục 2: xe ba bánh luôn là three_wheeler, kể cả có mui",v1.1` |
| `qc/QC_REPORT.md` | báo cáo QC (khuôn trong file) | |
| `guidelines/guideline_v1.1_calibrated.md` | copy `guideline/guideline_v1.0_label_contract.md` rồi sửa | |

Các file còn lại do **script** sinh ra: **không sửa tay**.
