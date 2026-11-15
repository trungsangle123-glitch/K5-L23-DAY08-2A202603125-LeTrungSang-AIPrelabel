# Submission — bài cá nhân

## Repo bài nộp

Mỗi học viên **một repo public**: fork repo đề, đổi tên theo mẫu.

| Mẫu tên repo | Ví dụ |
|---|---|
| `K5-L23-DAY08-[MSHV]-[HoTen]-AIPrelabel` | `K5-L23-DAY08-22001234-NguyenVanA-AIPrelabel` |

`HoTen` không dấu, viết liền. Theo hướng dẫn lớp nếu giảng viên đặt quy ước khác.

## Trước khi nộp

1. **Đổi dòng tiêu đề của `README.md`**:
   ```markdown
   # Day 08 Lab — 22001234 - Nguyễn Văn A
   ```
2. Điền [STUDENT.md](STUDENT.md) (kể cả "Kết quả tóm tắt").
3. Nộp link repo lên LMS **https://aithucchien.vinuni.edu.vn** hoặc kênh giảng viên/coach chỉ định.

Hạn nộp do giảng viên/coach thông báo.

## Cấu trúc bắt buộc

```text
README.md                          # dòng đầu: # Day 08 Lab — <MSHV> - <Họ và tên>
STUDENT.md                         # thông tin + kết quả tóm tắt
data/ATTRIBUTION.csv               # giữ nguyên
submission/
├── taxonomy.json                  # khớp guideline v1.1; KHÔNG đổi mục rules
├── recipe.md                      # recipe pre-label cuối (model, prompt, ngưỡng, segmenter, vì sao)
├── model_log.csv                  # >= 6 lần chạy, >= 3 model, có nhận xét
├── time_log.csv                   # thời gian thật: gold_manual, pilot_review, batch_review, seg_review
├── REPORT.md                      # báo cáo chính (6 mục)
├── individual_note.md             # ghi chú cá nhân, công cụ AI đã dùng
├── guidelines/
│   └── guideline_v1.1_calibrated.md
├── prelabel/
│   ├── pre_traps.coco.json        # file đã nạp vào CVAT (batch + gold, có bẫy)
│   ├── traps_key.json             # đáp án bẫy
│   └── seg_pre.coco.json          # pre-label mask của 8 ảnh seg
├── labels/
│   ├── gold_manual.json
│   ├── pilot_reviewed.json
│   ├── batch_reviewed.json
│   ├── seg_reviewed.json
│   ├── self_check_blind.json
│   └── qc_fixed.json              # (tuỳ chọn) ảnh sửa sau QC
├── release/                       # python scripts/build_release.py
│   ├── final_det.coco.json
│   ├── release_summary.csv
│   └── release_manifest.json
└── qc/
    ├── threshold_sweep.{csv,md,png}
    ├── review_stats.{json,md}, review_stats_seg.{json,md}
    ├── self_check.{json,md}, self_check_cases.csv
    ├── calibration_decisions.csv  # mỗi quyết định một dòng
    ├── qc_sample.csv, qc_review.csv, qc_report_auto.md
    └── QC_REPORT.md
```

**Không** commit: `work/`, `models/`, `*.pt`, token, mật khẩu, ảnh ngoài bộ dữ liệu.

## Checklist trước khi nộp

- [ ] Repo **public**, tên đúng quy tắc, mở được khi chưa đăng nhập.
- [ ] `README.md` tiêu đề đúng `MSHV - Họ và tên`; `STUDENT.md` điền đủ, kể cả kết quả tóm tắt.
- [ ] ≥ 5 commit bằng tài khoản của bạn, theo từng Part.
- [ ] `python scripts/validate_labels.py --all` sạch.
- [ ] `taxonomy.json` khớp `guideline_v1.1_calibrated.md`; mục `rules` không bị đổi.
- [ ] `model_log.csv`, `time_log.csv` là số thật; mỗi dòng log có nhận xét.
- [ ] `calibration_decisions.csv` ≥ 5 dòng; nội dung đã vào `guideline_v1.1_calibrated.md`.
- [ ] `QC_REPORT.md` điền đủ, tỉ lệ kèm mẫu số, có quyết định Release / Hold / Rework và giới hạn của mẫu nhỏ.
- [ ] `REPORT.md` có 3 quy tắc giảm thiên kiến và phần so sánh offline vs trực tiếp.
- [ ] `python scripts/check_submission.py` không còn `LỖI`.
- [ ] Không có token, `work/`, trọng số, hay dữ liệu ngoài phạm vi.
- [ ] Đã nộp link repo trước hạn.
