# Thông tin học viên

- Họ và tên: LeTrungSang
- MSHV: 2A202603125
- Lớp (L2 / L3 / khác): L2
- Tài khoản GitHub: trungsangle123-glitch
- Repo bài nộp (URL): https://github.com/trungsangle123-glitch/K5-L23-DAY08-2A202603125-LeTrungSang-AIPrelabel
- Commit chốt bài (hash): ca3ffe19371b7025ec4f0b0609c93b8f1d777cac
- Máy: Windows 11 Pro, NVIDIA GeForce RTX 3050 6 GB (CUDA 12.4, torch 2.6.0+cu124)
- CVAT (Docker): v2.81.0

## Kết quả tóm tắt (số lấy từ `submission/qc/*`, kèm mẫu số)

- Máy: accepted / edited / deleted: 224/232 = 96.6% / 1/232 = 0.4% / 7/232 = 3.0% (mẫu số: 232 box máy); added: 1/226 = 0.4% (mẫu số: 226 đối tượng sau duyệt)
- So với gold: precision / recall của **máy** 67.6% / 59.0% (23 TP, 11 FP, 16 FN; mẫu số 39 đối tượng gold trên 4 ảnh; KTC 95% 51–81% và 43–73%)
- Bắt bẫy: 12/12 = 100% (KTC 95%: 76–100%; ngưỡng đạt 80%)
- Thời gian: gán tay 17 phút / 4 ảnh = 4.25 phút/ảnh; duyệt có pre-label 20 phút / 24 ảnh = 0.83 phút/ảnh
- Lỗi QC: 0/5 = 0% theo ảnh, 0/53 = 0% theo đối tượng (mẫu ngẫu nhiên seed 42); cận trên Wilson 95% theo ảnh là 43%
- **Quyết định:** Release — lý do: 0/5 ảnh mẫu có lỗi (≤ 2%), bắt bẫy 12/12, không có lỗi hệ thống; nhưng cận trên 95% là 43% nên kết luận chỉ đúng trong giới hạn mẫu nhỏ 5 ảnh, cần nhắc trong REPORT.md.
