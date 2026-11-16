# Recipe pre-label cuối

> Điền sau Part 3. Mọi lựa chọn phải dẫn tới dòng trong `model_log.csv` hoặc bảng trong `qc/threshold_sweep.md`.

## 1. Model theo lớp

| Lớp | Model + cỡ | Prompt / ánh xạ | Ngưỡng | Vì sao chọn (dẫn `run_id`) |
|---|---|---|---|---|
| person | <<>> | <<>> | <<>> | <<>> |
| bicycle | <<>> | <<>> | <<>> | <<>> |
| motorbike | <<>> | <<>> | <<>> | <<>> |
| car | <<>> | <<>> | <<>> | <<>> |
| bus | <<>> | <<>> | <<>> | <<>> |
| truck | <<>> | <<>> | <<>> | <<>> |
| three_wheeler | <<>> | <<>> | <<>> | <<>> |

## 2. Lệnh tái lập (dán nguyên lệnh đã chạy)

```bash
<<các lệnh prelabel.py / merge_prelabels.py>>
```

## 3. Mask (SAM là bắt buộc)

- Phiên bản SAM đã chọn: <<SAM 1 (mobile_sam / sam_b) / SAM 2.1 (t/s/b/l) / SAM 3>>; lý do chọn: <<chất lượng mask, tốc độ, RAM, quyền truy cập>>
- Đã so với phiên bản nào khác (nếu có) và thấy gì: <<>>

## 4. Lỗi đã biết của recipe (không sửa được bằng ngưỡng)

- <<ví dụ: người ngồi trong tuk-tuk bị box gộp vào xe>>

## 5. Giới hạn

- <<pilot chỉ 6 ảnh; lớp nào có ít vật nên ngưỡng yếu>>
