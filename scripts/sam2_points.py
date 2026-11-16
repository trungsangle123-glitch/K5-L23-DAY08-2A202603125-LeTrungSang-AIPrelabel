"""SAM (bản bất kỳ: SAM 1 / SAM 2.1) với prompt là CLICK (giống công cụ Interactor trong CVAT): thử trên một ảnh, xem mask thay đổi theo click.

    python scripts/sam2_points.py --image img_013.jpg --pos 520,330 --neg 130,300 --out work/sam2_click
    python scripts/sam2_points.py --image img_013.jpg --pos 520,330 --box 90,30,960,640 --out work/sam2_click

--pos x,y  : click dương (thuộc vật)    [dùng nhiều lần được]
--neg x,y  : click âm (KHÔNG thuộc vật) [dùng nhiều lần được]
--box x1,y1,x2,y2 : khung gợi ý (tuỳ chọn)
Toạ độ là pixel trên ảnh gốc (mở ảnh bằng trình xem ảnh bất kỳ và rê chuột; hoặc thử rồi nhìn kết quả).
Ghi <out>/<name>.jpg (mask tô màu, chấm xanh = dương, chấm đỏ = âm) và in diện tích mask / số polygon.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from common import IMAGES_DIR, ROOT, die, mask_to_polys, pick_device, rel
from prelabel import weights_path


def pt(s: str):
    try:
        x, y = s.split(",")
        return float(x), float(y)
    except ValueError:
        die(f"Sai định dạng toạ độ '{s}': cần x,y (ví dụ 520,330).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--image", required=True, help="tên ảnh trong data/images/")
    ap.add_argument("--pos", action="append", default=[])
    ap.add_argument("--neg", action="append", default=[])
    ap.add_argument("--box")
    ap.add_argument("--sam", "--sam2", dest="sam", default="sam2.1_b.pt", help="mobile_sam.pt | sam_b.pt (SAM 1) | sam2.1_t/s/b/l.pt (SAM 2.1)")
    ap.add_argument("--device", default="auto")
    ap.add_argument("--out", required=True)
    ap.add_argument("--name", default="mask_overlay", help="tên file ảnh kết quả (không đuôi), ví dụ tuktuk_img013")
    a = ap.parse_args()
    path = IMAGES_DIR / a.image
    if not path.exists():
        die(f"Không thấy {rel(path)}")
    if not a.pos and not a.box:
        die("Cần ít nhất một --pos hoặc --box.")
    from ultralytics import SAM
    model = SAM(weights_path(a.sam))
    pts = [pt(s) for s in a.pos] + [pt(s) for s in a.neg]
    labels = [1] * len(a.pos) + [0] * len(a.neg)
    kw = {}
    if pts:
        kw["points"] = [pts]
        kw["labels"] = [labels]
    if a.box:
        kw["bboxes"] = [list(map(float, a.box.split(",")))]
    r = model(str(path), device=pick_device(a.device), verbose=False, **kw)[0]
    if r.masks is None or len(r.masks.data) == 0:
        die("SAM không trả mask nào: thử click vào giữa vật hơn.")
    m = r.masks.data[0].cpu().numpy() > 0.5
    im = Image.open(path).convert("RGB")
    ov = np.array(im).astype(np.float32)
    ov[m] = ov[m] * 0.45 + np.array([230, 25, 75], np.float32) * 0.55
    out = Image.fromarray(ov.astype(np.uint8))
    d = ImageDraw.Draw(out)
    for (x, y), l in zip(pts, labels):
        c = (0, 200, 0) if l else (255, 0, 0)
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=c, outline="white", width=2)
    if a.box:
        d.rectangle(list(map(float, a.box.split(","))), outline="yellow", width=2)
    o = Path(a.out)
    o.mkdir(parents=True, exist_ok=True)
    out.save(o / f"{a.name}.jpg", quality=90)
    polys = mask_to_polys(m.astype(np.uint8))
    print(f"Mask: {int(m.sum())} px ({m.sum() / m.size * 100:.1f}% ảnh), {len(polys)} polygon -> {rel(o / f'{a.name}.jpg')}")


if __name__ == "__main__":
    main()
