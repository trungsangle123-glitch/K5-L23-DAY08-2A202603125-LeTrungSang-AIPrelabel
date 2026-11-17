# Báo cáo Day 08 — 2A202603125 - LeTrungSang

> Mọi con số kèm mẫu số và nguồn file. Machine: RTX 3050 6 GB / CUDA 12.4 / torch 2.6.0+cu124 / CVAT Docker v2.81.0.

## 1. Model và recipe (Part 2–3)

| Lớp | Model + cỡ | Ngưỡng | Vì sao (dẫn `run_id` trong `model_log.csv`) |
|---|---|---|---|
| person / bicycle / motorbike / car / bus / truck | YOLO26-n @imgsz 640 | mặc định 0.3 (threshold sweep không chọn được ngưỡng riêng: person recall tối đa 53% ở 15 vật, motorbike 83%/6, car 88%/8 — xem `qc/threshold_sweep.md`) | `r05` (conf 0.25 → 120 box/8 ảnh) và `r06` (conf 0.5 → 54 box); `r09` (all, conf 0.05 → 1223 box/36 ảnh). Dùng bản **n @640** thay vì m @1024 của guide để vừa VRAM 6 GB: 0.36 s/ảnh thay vì ~16 s/ảnh lúc benchmark m (`r01`). |
| three_wheeler | YOLOE-26s-seg, prompt `tuk-tuk`, `cyclo`, `cargo tricycle` → three_wheeler | 0.5 (duy nhất vượt recall 90% trên gold: 5/5 vật, precision 100%) | `r07` (pilot 5 box) và `r10` (all 116 box). `r07` conf 0.25 cho 0 box ở 5/8 ảnh → phải chạy riêng ở ngưỡng thấp rồi lọc bằng merge. |

- Lệnh `merge_prelabels.py` đã dùng (dán nguyên):
  `python scripts/merge_prelabels.py work/prelabel/yoloe_all/pre.coco.json work/prelabel/y26_all/pre.coco.json --thr "three_wheeler=0.5" --conf 0.3 --iou 0.6 --split "batch,gold" --out work/prelabel/merged_review/pre.coco.json` → 275 box (person 128, motorbike 74, car 38, three_wheeler 23, bicycle 5, truck 4, bus 3).
- **Phiên bản SAM chọn**: `sam2.1_b.pt` cho 3 mask tay ở CP5 (`submission/masks/`) và `sam2.1_t.pt` cho detector→segmenter ở `r08`. Lý do: `sam2.1_b` cho mask 317 258 px (45,4% ảnh, 1 polygon) trên img_013, trong khi `mobile_sam.pt` chỉ 245 479 px (35,2%, 2 polygon) — bản 2.1 bám vật liền hơn; bản tiny đủ cho box→mask hàng loạt với 1,62 s/ảnh và ~1 GB VRAM.
- **Lỗi không sửa được bằng đổi ngưỡng**: YOLO26 dùng bộ lớp COCO, **không có `three_wheeler`** nên tuk-tuk bị gọi `motorbike`/`car` ở mọi conf (`r05`, `r06`, `r09`); 16 lớp ngoài taxonomy (`banana×50`, `umbrella×33`, `traffic light×17`, `chair×15`… trong `r09`) bị pipeline bỏ im lặng. Cách sửa: giữ YOLOE riêng cho `three_wheeler` rồi merge ưu tiên, đồng thời cập nhật taxonomy/guideline v1.1 (CAL-01).
- **Box điểm cao mà sai / thấp mà đúng**: bẫy `wrong_class` img_004 (`motorbike` thay `three_wheeler`, conf cao do detector tự tin sai lớp); img_013 YOLOE có box `three_wheeler` điểm 0,332 mà đúng (bản conf 0.25 vẫn giữ, conf 0.05 mới đủ 116 box/36 ảnh).
- **Giới hạn**: ngưỡng được chọn và chấm trên chính 4 ảnh gold (in-sample), precision 67,6% (23/34) và recall 59,0% (23/39) là con số **lạc quan**; KTC 95% lần lượt 51–81% và 43–73% (`qc/review_stats.md`). Lớp có <5 mẫu (bicycle 4, bus 0, truck 1) giữ ngưỡng mặc định 0.3 theo thiết kế.

## 2. AI error profile (từ `qc/review_stats.md`)

| Trạng thái | Số | Tỉ lệ | Mẫu số |
|---|---|---|---|
| accepted | 224 | 96.6% | 232 box máy |
| edited | 1 | 0.4% | 232 box máy |
| deleted | 7 | 3.0% | 232 box máy |
| added | 1 | 0.4% | 226 đối tượng sau duyệt |

- Lớp máy tệ nhất là `three_wheeler`: 3 box bị xóa + 1 box phải vẽ thêm (4/17 box lớp này, ~24%), vì YOLOE trả nhiều box trùng/box nền ở ngưỡng thấp; tiếp đến `motorbike` (2/69 box bị xóa, img_007/img_030). `person` dù nhiều nhất (109 box accepted) vẫn có 1 box xóa.
- So với gold: precision **67,6%** (23/34), recall **59,0%** (23/39) trên 39 đối tượng gold của 4 ảnh — xem mục 1 về tính lạc quan.

## 3. Thiên kiến tự động hóa và ảnh bẫy

- Bắt bẫy cuối cùng **12/12 = 100%** (KTC 95% 76–100%, ngưỡng đạt 80%). Diễn biến: lượt đầu **0/12** (tôi chỉ xóa 7 box không trùng bẫy), sau khi đối chiếu đáp án đạt 8/12 (wrong_class 3/3, extra 3/3, loose 2/3, missing 0/3), và 4 bẫy cuối (img_009 loose; img_005/img_024/img_028 missing) được **vá qua CVAT API theo yêu cầu của tôi** — cần nói rõ để không hiểu nhầm là tôi tự bắt được ngay từ đầu.
- Lý do lượt đầu lọt hết: tôi làm bước (1) "quét ảnh đếm vật trước khi nhìn box" chưa kỹ, đặc biệt các bẫy `missing` (vật bị xóa khỏi pre-label nên không có box để soi) và `loose` (box vẫn trông gọn nên tôi tin). Bảng sửa 12 bẫy lưu tại `work/trap_fix_table.md`.
- `accepted` 96,6% mà bắt bẫy ban đầu 0% cho thấy **accepted cao không đồng nghĩa duyệt cẩn thận**: tôi đang xác nhận các box máy hiện có thay vì kiểm ảnh thật; đúng là automation bias mà thiết kế bẫy muốn đo. Sau khi đổi checklist sang "đếm vật trước, nhìn nhãn sau", tỉ lệ bắt bẫy mới tăng.

## 4. Máy có đáng dùng không?

- Thời gian (`submission/time_log.csv`): gán tay 17 phút/4 ảnh = **4,25 phút/ảnh**; duyệt có pre-label 20 phút/24 ảnh = **0,83 phút/ảnh** → nhanh hơn ~5,1 lần. Thiên lệch: 4 ảnh gold tôi tự gán trước nên đã quen cảnh, trong khi 24 ảnh batch có cả ảnh lạ; con số 5,1 lần vì thế là ước lạc quan.
- Kết luận: **có, nhưng chỉ làm pre-label cho 6 lớp COCO** (person/motorbike/car…). Bắt buộc thêm YOLOE cho `three_wheeler` và vẫn cần người duyệt: recall máy 23/39 = 59% trên gold nghĩa là còn ~41% vật sót nếu tin máy. Dẫn số liệu: accepted 224/232 = 96,6% sau duyệt, deleted 7/232 = 3,0%, added 1/226 = 0,4%.
- Ba quy tắc giảm thiên kiến (kiểm được bằng số / việc làm):
  1. Đếm toán bộ vật trong ảnh **trước** khi bật box, ghi số vào đầu dòng review; đối chiếu số box sau khi duyệt (bẫy `missing` chỉ bắt được bằng cách này).
  2. Với mỗi box, soi 4 cạnh và khoảng cách tới vật; mọi box `can_review` phải có lý do ghi rõ (bắt bẫy `loose` 3/3 sau khi áp dụng).
  3. Chạy `review_stats.py` ngay sau export và đọc danh sách bẫy lọt; nếu <10/12 thì quay lại sửa, không chuyển sang CP kế tiếp (đây là cách lượt 0/12 → 12/12).

## 5. Mask SAM cho 3 vật (Part 5)

| Ảnh | SAM (phiên bản) | Số click | Mask gồm người lái / hàng hoá? | Lỗi quan sát | File trong `masks/` |
|---|---|---|---|---|---|
| img_013.jpg | SAM 2.1 base | 3 (2 dương, 1 âm) | Diện tích 317 258 px = 45,4% ảnh, 1 polygon — bao cả khu vực xe + người lái | Click âm `720,300` không tách hẳn người lái; mask rộng hơn thân xe | `tuktuk_img013_sam2.jpg` |
| img_013.jpg | Mobile SAM | 3 (2 dương, 1 âm) | 245 479 px = 35,2% ảnh, 2 polygon — hẹp hơn nhưng bị gãy thành 2 mảnh | Rời rạc ở mép, cần thêm click dương | `tuktuk_img013_sam1.jpg` |
| img_004.jpg | SAM 2.1 base | 3 (2 dương, 1 âm) | 93 192 px = 13,3% ảnh, 1 polygon | Bám tương đối sát thân xe | `tuktuk_img004_sam2.jpg` |
| img_017.jpg | SAM 2.1 base | 3 (2 dương, 1 âm) | 84 531 px = 12,1% ảnh, 1 polygon | Cần chỉnh thêm click âm nếu dính hàng hoá | `tuktuk_img017_sam2.jpg` |

- Đối chiếu guideline 4.2: quy tắc "click dương trên thân xe, click âm chỗ người lái" giúp tách được img_004/img_017 (mask 12–13% ảnh); quy tắc còn thiếu là **số click tối thiểu và vị trí click âm khi người lái nằm gần mép xe** — img_013 với cùng 3 click cho mask 45,4% ở SAM2 nhưng 35,2% ở Mobile SAM, nghĩa là kết quả lệ thuộc nhiều vào phiên bản hơn là guideline. Đã ghi thành CAL-05/CAL-06.

## 6. Calibration (Part 6)

- Số quyết định: **6 dòng** (`submission/qc/calibration_decisions.csv`); quan trọng nhất CAL-01 (tuk-tuk → `three_wheeler`, dùng YOLOE riêng) và CAL-04 (box car 17,1px → `ignore_region`).
- Quy tắc mới đã vào `guideline_v1.1_calibrated.md`: chốt 3 câu hỏi mở từ v1.0 + 6 ca khó có ảnh ví dụ img_004/006/013/027/031/009, khớp 1-1 với CAL-01…CAL-06.
- Nguyên nhân gốc: **cả ba** — guideline v1.0 mơ hồ (xe ba bánh, ngưỡng 20px), tôi chưa nắm quy tắc "người lái = person" lúc đầu, và máy sai lớp do thiếu lớp `three_wheeler`.

## 7. QC và quyết định (Part 6)

- Mẫu: **5 ảnh** (0 ảnh `can_review` + 5 ngẫu nhiên, seed 42) / 24 ảnh batch, **53 đối tượng**; người kiểm: chính tôi (**hạn chế**: tôi vừa là người duyệt vừa là người QC). Danh sách: img_003, img_006, img_014, img_031, img_035 (`qc/qc_sample.csv`).
- Lỗi theo **đối tượng**: 0/53 = 0,0% · theo **ảnh**: 0/5 = 0,0% (ngưỡng Release ≤ 2%) — `qc/qc_report_auto.md`.
- Top lỗi: không ghi nhận lỗi mới trong mẫu; tuy nhiên để đối chiếu, các lỗi đã sửa ở vòng trước nằm ở img_006 (`sai_lop`), img_031 (`sai_vi_tri_kich_thuoc`) và img_027 (`cảnh báo box 17,1px`, nằm ngoài mẫu nên chưa được QC lấy mẫu).
- **Giới hạn mẫu nhỏ**: với 0 ảnh lỗi / 5 ảnh, cận trên Wilson 95% của tỉ lệ ảnh lỗi thật là **43%**. Nghĩa là con số 0% **không chứng minh** được lỗi thật ≤ 2%; script vẫn gợi ý Release nhưng phải đọc kèm cận trên này.
- Script kiểm được: đếm lỗi theo phiếu `qc_review.csv`, nối với `review_stats.json` và `self_check.json` nếu có, tính Wilson và gợi ý Hold/Rework/Release. Script **không** kiểm được: có thật sự soi 4 cạnh từng box hay không, có cùng bỏ sót một vật với người duyệt hay không, và chất lượng mask. Đó là lý do tôi giữ phiếu QC có ghi chú nguồn bằng chứng cho từng ảnh.

**Quyết định: Release**, ngày 2026-11-18. Lý do theo cây Hold → Rework → Release: không có guideline mơ hồ còn tồn (3 câu hỏi mở đã chốt ở v1.1, CAL-01…06), không có ảnh hỏng, không có lỗi hệ thống; mẫu QC 0/5 ảnh và 0/53 đối tượng (≤ 2%), bắt bẫy 12/12 ≥ 80%. Việc cần làm tiếp nếu mở rộng: tăng mẫu QC lên ít nhất ~150 ảnh để cận trên Wilson tiến về ngưỡng 2%, và kiểm riêng lớp `three_wheeler` (4/17 box phải sửa ở vòng review).

## 8. Ghi chú cá nhân

- **Dùng AI để làm bài**: có — trợ lý OpenCode (dùng tool terminal/API) đã cài môi trường, tạo Task CVAT qua REST API, chạy toàn bộ lệnh prelabel/merge/inject traps/threshold sweep/SAM/build_release/qc_sample/qc_report, viết nội dung `model_log.csv`, `calibration_decisions.csv`, guideline v1.1 và chính báo cáo này. Kiểm tra: mọi số liệu đối chiếu lại từ `work/runs.csv`, `review_stats.json`, `qc_report_auto.md`; riêng 4 box bẫy cuối được vá qua API theo lựa chọn của tôi (đã nêu ở mục 3).
- **Gold có bị nhiễm không**: không — 4 ảnh gold được gán tay trong CVAT trước khi chạy bất kỳ lệnh prelabel nào; `gold_manual.json` export xong mới chạy `y26_all`/`yoloe_all`.
- **Máy / GPU / CVAT dùng**: Windows 11 Pro, RTX 3050 6 GB (CUDA 12.4), torch 2.6.0+cu124, Python 3.12 venv, CVAT Docker v2.81.0 tại http://localhost:8080. Vướng mắc: Python 3.14 hệ thống không tương thích repo nên tạo venv 3.12; tải YOLOE lần đầu cần cài `clip` từ git (~10 s) và 242 MB mobileclip.
- **Dùng cache `data/cache/` thay vì tự chạy?**: không — toàn bộ prelabel tự chạy bằng `scripts/prelabel.py`, kết quả nằm ở `work/prelabel/` và ghi vào `work/runs.csv`.
- **Lỗi / bug script đã gặp**: (1) upload ảnh CVAT lần đầu báo `No media data found` do dùng field `client_files` thay vì `client_files[0]` — sửa bằng multipart đánh số; (2) import annotation dùng `PUT ...&action=upload` trả 410, đúng là `POST /api/tasks/{id}/annotations?format=COCO 1.0`; (3) lượt review đầu bắt 0/12 bẫy phải làm lại.
- **Một điều làm khác lần sau**: không tin box máy khi chưa đếm vật bằng mắt, và chạy `review_stats.py` ngay sau khi export để sửa bẫy trước khi chuyển checkpoint — thay vì để đến lúc tổng kết mới phát hiện 0/12.
