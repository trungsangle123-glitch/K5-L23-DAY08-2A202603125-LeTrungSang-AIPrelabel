# Calibration và QC (Part 3, 6)

Calibration = làm cho **máy, guideline và bạn** nhất quán, **có số đo và bằng chứng**. Trong bài này có bốn tầng:

| Tầng | Chỉnh cái gì | Công cụ | Sản phẩm |
|---|---|---|---|
| 1. Ngưỡng | ngưỡng tin cậy **theo lớp** của pre-label | `threshold_sweep.py` trên pilot | `qc/threshold_sweep.*`, `recipe.md` |
| 2. Guideline | quy tắc nào mơ hồ / thiếu, từ lỗi của máy và của bạn | `calibration_decisions.csv`, v1.1 | `guideline_v1.1_calibrated.md` |
| 3. Nhất quán | bạn gán **lại mù** có giống bản đã duyệt không | `self_consistency.py` | `qc/self_check.*` |
| 4. Chất lượng | mẫu QC, Release / Hold / Rework | `qc_sample.py`, `qc_report.py` | `QC_REPORT.md` |

## Tầng 1 — Ngưỡng theo lớp (pilot)

Không có ngưỡng hoàn hảo, chỉ có **đánh đổi**: ngưỡng thấp → nhiều box thừa (mất công xoá); ngưỡng cao → bỏ sót (lỗi lọt vào dataset, khó thấy).
Chọn ngưỡng **theo từng lớp** trên pilot đã có nhãn chuẩn:

```bash
# pre-label pilot (đã gộp, ngưỡng 0.10), duyệt bằng CVAT, export pilot_reviewed.json (Part 3), rồi:
python scripts/threshold_sweep.py --pred work/prelabel/merged_pilot/pre.coco.json --gold submission/labels/pilot_reviewed.json
```

- Bảng precision / recall từng lớp ở mỗi ngưỡng → `qc/threshold_sweep.csv` + hình `.png`.
- **Ngưỡng gợi ý** = cao nhất mà recall còn ≥ mục tiêu (`recall_target` = 0.9): ít box thừa nhất khi chưa bỏ sót thêm.
- **Giới hạn của phép đo**: nhãn chuẩn pilot được dựng từ pre-label ngưỡng 0.10 rồi sửa tay, nên vật có điểm < 0.10 và bạn không tự vẽ thì vắng mặt trong GT (recall thật thấp hơn recall đo được); dải ngưỡng quét bắt đầu từ 0.10 vì dưới đó không đo được gì.
- **Mẫu nhỏ**: pilot có 6 ảnh; lớp nào có ít vật (xem cột `n_gold`) thì ngưỡng của lớp đó chỉ là ước lượng thô. Hãy nói rõ trong báo cáo. Lớp không có vật nào trong pilot thì giữ ngưỡng mặc định.
- Dán `--thr ...` in ra vào `merge_prelabels.py`.

## Tầng 2 — Calibration guideline

Nguồn của các "ca" cần quyết (mỗi nguồn là một nơi guideline có thể mơ hồ):

1. 7 câu hỏi **còn mở** ở mục 6 của guideline v1.0.
2. Box bạn **tick `can_review`**.
3. Cụm lỗi lặp lại của máy: `deleted` / `added` cao ở một lớp, `class_changed` (đổi lớp) trong `review_stats.md`.
4. Bẫy bạn **để lọt** (`review_stats.md` mục 3).
5. Ca lệch trong `self_check_cases.csv` (tầng 3).

Mỗi ca đã quyết là **một dòng** trong `submission/qc/calibration_decisions.csv`:

| Cột | Ý nghĩa |
|---|---|
| `case_id` | `CAL-01`, `CAL-02`, … |
| `image` | ảnh ví dụ (`img_0xx`; nhiều ảnh cách nhau `|`) |
| `nguon` | một trong: `cau_hoi_mo`, `can_review`, `loi_may`, `bay_lot`, `self_check` |
| `van_de` | tình huống, một câu |
| `quyet_dinh` | bạn quyết thế nào |
| `quy_tac_ghi_vao_guideline` | câu quy tắc đã viết vào v1.1 (mục nào) |
| `phien_ban_guideline` | ví dụ `v1.1` |

**Yêu cầu tối thiểu: ≥ 5 dòng**, gồm ít nhất **một** từ `loi_may` và **một** từ `cau_hoi_mo`. Quyết định nào là quy tắc mới phải **thật sự nằm** trong `guideline_v1.1_calibrated.md` (đối chiếu bằng mắt người chấm).
Hỏi: **guideline mơ hồ** (cần sửa chữ) hay **tôi / máy làm sai** (không cần đổi guideline)? Chỉ cái thứ nhất mới vào v1.1.

Nếu quyết định thay đổi **nhãn đã gán** (ví dụ chuyển hẳn xe đạp điện sang `motorbike`), sửa nhãn trong CVAT, export lại `batch_reviewed.json` hoặc `qc_fixed.json` (ảnh đã sửa), rồi `python scripts/build_release.py`.

## Tầng 3 — Gán lại mù (nhất quán của chính bạn)

Sau ≥ 60 phút kể từ khi duyệt xong (hoặc hôm sau), **gán tay không AI**, theo guideline **v1.0** (bản bạn đã dùng lúc gán; v1.1 chưa viết), 8 ảnh bạn đã duyệt, **không mở lại** nhãn cũ:

```bash
python scripts/prepare_workdirs.py --selfcheck       # work/tasks/selfcheck/: 8 ảnh batch (bỏ ảnh quá dày)
# Task mới "selfcheck-blind" từ thư mục đó, gán theo guideline v1.0, export -> submission/labels/self_check_blind.json
python scripts/self_consistency.py --a submission/labels/batch_reviewed.json --b submission/labels/self_check_blind.json
```

Đạt khi IoU trung bình ≥ 0.85, cùng lớp ≥ 95% **và** tỉ lệ box không ghép được ≤ 10% (mẫu số: số cặp box ghép được / tổng box; ghi cả ba trong báo cáo). IoU chỉ tính trên cặp đã ghép (IoU ≥ 0.5) nên **luôn đọc cùng tỉ lệ không ghép được**. Mỗi dòng của `self_check_cases.csv` là ứng viên cho tầng 2.
Hiểu đúng: bạn lệch với **chính mình** ở đâu → đó là chỗ guideline mơ hồ hoặc bạn chưa nắm quy tắc. **Có bạn học?** Hai người đổi file và chạy `--a` của bạn, `--b` của họ: cũng là đo đồng thuận giữa hai người (tuỳ chọn, cộng điểm cho phân tích).

## Tầng 4 — QC mẫu và quyết định

```bash
python scripts/build_release.py                       # nhãn cuối của 24 ảnh batch
python scripts/qc_sample.py --n 8 --seed 42           # mẫu = mọi ảnh có can_review + 8 ảnh ngẫu nhiên
# mở work/qc/review/*.jpg (id từng vật in sẵn), điền submission/qc/qc_review.csv
python scripts/qc_report.py                           # --guideline-gap N / --data-problem N nếu có
```

`qc_review.csv`: mỗi lỗi **một dòng**: `image, object_id, error_type, reviewer, note`.
`error_type` chỉ nhận: `khong` (ảnh sạch), `bo_sot`, `thua`, `sai_lop`, `sai_vi_tri_kich_thuoc`, `sai_thuoc_tinh`, `sai_mask`. Lỗi bỏ sót không có id thì để trống `object_id` và mô tả trong `note`.
Ảnh nào còn `error_type` trống bị coi là **chưa kiểm**.

**Quy ước số đo (luôn ghi mẫu số):**

| Chỉ số | Công thức | Ghi chú |
|---|---|---|
| Lỗi theo **đối tượng** | đối tượng lỗi / đối tượng trong mẫu | ví dụ `3/163 = 1.8%` |
| Lỗi theo **ảnh** | ảnh có ≥ 1 lỗi / ảnh trong mẫu | ngưỡng Release ≤ 2% |
| Accepted / edited / deleted | ÷ **box máy** | trạng thái của máy |
| Added | ÷ **đối tượng sau duyệt** | máy sót bao nhiêu (≈ 1 − recall) |
| Bắt bẫy | bẫy sửa đúng / tổng bẫy | ≥ 80% (≥ 10/12) |
| IoU TB / cùng lớp (tầng 3) | trên cặp box ghép được | 0.85 / 95% |

**Hiểu từng số trong `review_stats.md`:**

| Thấy | Nghĩa là | Việc làm |
|---|---|---|
| `deleted` cao | ngưỡng quá thấp, hoặc ánh xạ nhãn sai | tăng ngưỡng lớp đó; kiểm `--map` / prompt |
| `added` cao | máy bỏ sót nhiều (ở lớp nào?) | hạ ngưỡng, thêm lượt tìm vật sót, đổi model |
| `accepted` thấp (< 50%) | sửa mỗi box lâu hơn vẽ mới | đổi model / ngưỡng; vẽ tay lớp đó |
| Recall của **máy** trên gold thấp | máy sót nhiều → `added` của batch sẽ cao | hạ ngưỡng, đổi model |
| Precision của **máy** trên gold thấp | nhiều box thừa → `deleted` cao | tăng ngưỡng |
| Bắt bẫy thấp dù `accepted` cao | bạn **không bắt lỗi của máy** (thiên kiến tự động hóa) | siết bước 0 của checklist |
| (nâng cao, có `gold_reviewed`) `residual` cao | bạn giữ lại lỗi của máy | xem bẫy lọt |

**Cây quyết định (đi từ trên xuống):**

1. Guideline chưa rõ (còn câu hỏi chưa chốt) hoặc dữ liệu hỏng? → **Hold**.
2. > 2% ảnh có lỗi, **hoặc** lỗi lặp lại cùng một kiểu (≥ 3 lỗi và ≥ 50% cùng loại), **hoặc** bắt bẫy < 80%, **hoặc** nhất quán dưới ngưỡng? → **Rework**.
3. Còn lại → **Release**.

> **Giới hạn thống kê:** mẫu QC chỉ khoảng 10 ảnh. Nếu **0 lỗi** trong n ảnh, tỉ lệ ảnh lỗi thật vẫn có thể tới ~3/n (quy tắc 3, 95%). Ví dụ 0/10 ảnh thì lỗi thật có thể tới ~30%.
> Vì vậy kết luận "đạt 2%" trên mẫu nhỏ là **yếu**: hãy viết rõ giới hạn này. Chọn Rework trung thực **không bị trừ điểm**; **báo Release khi số liệu không đạt thì bị trừ**.
> Nếu quyết định **Rework**: sửa lỗi, cập nhật nhãn (`qc_fixed.json`), chạy lại bước tương ứng và ghi vòng sau vào báo cáo.

## Script kiểm được gì, không kiểm được gì

Kiểm được: tên file, lớp có trong taxonomy, box trong ảnh, đủ ảnh được giao, accepted/edited/deleted/added, độ lệch giữa hai bộ nhãn, các số đo QC.
**Không** kiểm được: box có **ôm sát vật thật** không, lớp có đúng thực tế không, vật mà **cả bạn lẫn máy** cùng bỏ sót (ngoài gold), việc bạn có theo checklist thật hay không.
Những việc đó cần mắt người đối chiếu với guideline và ảnh gốc.
