# Rubric — 100 điểm

Điểm dựa trên **bằng chứng trong repo và chất lượng phân tích**, **không** dựa vào việc số đo đẹp hay được Release.
Bắt bẫy 60% mà phân tích trung thực nguyên nhân tốt hơn 100% mà không giải thích được.

| # | Hạng mục | Điểm | Bằng chứng |
|---|---|---:|---|
| 1 | Cài đặt, tái lập, git | 8 | `check_submission.py`, commit, `STUDENT.md`, README |
| 2 | Gold gán tay và dùng label contract | 10 | `labels/gold_manual.json`, `time_log.csv`, `individual_note.md` |
| 3 | Tour model và recipe | 20 | `model_log.csv`, `recipe.md`, `REPORT.md` mục 1 |
| 4 | Pilot và ngưỡng theo lớp | 10 | `pilot_reviewed.json`, `qc/threshold_sweep.*`, `recipe.md` |
| 5 | Review và đo (batch, bẫy, AI error profile) | 20 | `batch_reviewed.json`, `qc/review_stats.*`, `REPORT.md` mục 2–4 |
| 6 | Segmentation và CVAT trực tiếp | 10 | `seg_reviewed.json`, `qc/review_stats_seg.*`, `REPORT.md` mục 5 |
| 7 | Calibration (guideline, nhất quán) | 12 | `calibration_decisions.csv`, `guideline_v1.1`, `qc/self_check.*` |
| 8 | QC và báo cáo | 10 | `QC_REPORT.md`, `qc_review.csv`, `release/` |

## 1. Cài đặt, tái lập, git (8)
- 3: `check_submission.py` không còn `LỖI`; repo public, tên đúng, README tiêu đề đúng.
- 3: ≥ 5 commit theo từng Part, bằng tài khoản của bạn; không commit `work/`, trọng số, token.
- 2: `STUDENT.md` đầy đủ; `individual_note.md` ghi rõ công cụ AI đã dùng và cách kiểm tra.
- *Mất điểm:* lộ token; commit file nặng; commit gộp một lần cuối.

## 2. Gold và label contract (10)
- 4: `gold_manual.json` hợp lệ (đủ 6 ảnh, qua `validate_labels`), gán **trước** khi thấy nhãn máy (ghi trung thực nếu bị nhiễm).
- 3: `can_review` dùng đúng nghĩa (ca **không chắc quy tắc**), có ghi các ca khó theo ảnh (`img_0xx`).
- 3: `time_log.csv` có `gold_manual` thật.
- *Mất điểm:* gold giống hệt pre-label đến từng pixel (nghi dùng AI); tick `can_review` cho mọi box.

## 3. Tour model và recipe (20)
- 6: ≥ 6 lần chạy, ≥ 3 model khác nhau (closed-set, SAM, open-vocab); mỗi dòng có thông số đủ để chạy lại.
- 8: `what_went_wrong` **cụ thể** (ảnh, vật, loại lỗi), không chung chung; có so sánh giữa model / ngưỡng / prompt.
- 6: `recipe.md`: lớp nào dùng model nào và **vì sao**, dựa trên `model_log`; hiểu được lỗi nào **không** sửa bằng ngưỡng (tuk-tuk → car/truck).
- *Mất điểm:* chỉ chạy lệnh trong hướng dẫn, không quan sát; số liệu `model_log` không khớp `work/runs.csv` / không tái lập được.

## 4. Pilot và ngưỡng (10)
- 4: nhãn pilot qua checklist, `pilot_reviewed.json` hợp lệ.
- 4: `threshold_sweep` chạy, ngưỡng **theo lớp**, nói rõ giới hạn do mẫu nhỏ / lớp không có vật.
- 2: ngưỡng trong `recipe.md` khớp bảng sweep (hoặc giải thích vì sao khác).
- *Mất điểm:* dùng gold để chọn ngưỡng; một ngưỡng chung không lý do.

## 5. Review và đo (20)
- 4: `batch_reviewed.json` hợp lệ (24 ảnh batch), đã nạp đúng `pre_traps`.
- 6: đọc **đúng** `review_stats` (mẫu số, vì sao loại vùng bẫy khỏi profile, precision-recall của máy so với gold); trả lời máy có đáng dùng không dựa trên `time_log` + `accepted`.
- 5: phân tích bẫy lọt (loại nào, vì sao, bước checklist nào bị bỏ) và liên hệ thiên kiến tự động hóa.
- 5: 3 quy tắc giảm thiên kiến **kiểm tra được**.
- *Mất điểm:* mở `traps_key.json` trước; sửa tay số đo; nói "accepted cao = máy tốt" mà không nhắc tới sót (added, recall trên gold).

## 6. Segmentation và CVAT trực tiếp (10)
- 4: `seg_reviewed.json` có polygon, qua `validate_labels --mode seg`; `review_stats_seg` chạy.
- 3: phân tích mask: lỗi hay gặp (người lái, hàng hoá, lỗ thủng, bóng) và quy tắc đã dùng.
- 3: thử ít nhất một cách trực tiếp (B1 / B3 / B2) và ghi **trung thực** kết quả (kể cả không chạy được: lỗi + đã thử gì).

## 7. Calibration (12)
- 5: `calibration_decisions.csv` ≥ 5 dòng, mỗi dòng có nguồn và quyết định; có ít nhất một ca `loi_may` và một ca `cau_hoi_mo`.
- 4: `guideline_v1.1` **thật sự chứa** quy tắc của các quyết định; mỗi ca khó mới có ảnh ví dụ; bảng lịch sử đúng.
- 3: `self_check` chạy, giải thích ca lệch (guideline mơ hồ hay bạn bất cẩn).
- *Mất điểm:* quyết định không vào v1.1; v1.1 mâu thuẫn với nhãn đã nộp.

## 8. QC và báo cáo (10)
- 3: mẫu và cách chọn; **hai cách đếm tỉ lệ lỗi kèm mẫu số**.
- 3: quyết định theo cây Hold → Rework → Release và **khớp số liệu**; nêu giới hạn thống kê của mẫu nhỏ.
- 2: top lỗi có ảnh ví dụ; phần "script kiểm được và không kiểm được" thực chất.
- 2: `REPORT.md` đủ mục, đọc được, không chép nguyên output của script.
- *Mất điểm:* báo Release khi số liệu không đạt; chỉ ghi % không mẫu số.

## Trừ điểm chung
- Thiếu thành phần: chỉ chấm phần có bằng chứng.
- **Số liệu giả** (nhãn, thời gian, bẫy, log model): 0 điểm phần liên quan, báo giảng viên.
- Nộp muộn, sai tên repo, sai link: theo [RULES.md](RULES.md).
