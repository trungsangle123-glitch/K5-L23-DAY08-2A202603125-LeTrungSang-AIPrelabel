"""Sinh JSON nhãn để dán vào CVAT (Project -> Labels -> tab Raw) từ submission/taxonomy.json.

    python scripts/make_cvat_labels.py

Ghi cvat/labels_generated.json. Nhãn trong CVAT PHẢI trùng tên với taxonomy (script map theo tên lớp).
"""
from __future__ import annotations

import json

from common import ROOT, load_taxonomy, rel

COLORS = ["#e6194b", "#3cb44b", "#4363d8", "#f58231", "#911eb4", "#46c8c8", "#f032e6", "#9a6324", "#808000"]


def main() -> None:
    tax = load_taxonomy()
    labels = []
    for i, name in enumerate(tax.classes):
        attrs = []
        if name != tax.ignore:
            for a in tax.attrs.values():
                attrs.append({"name": a["name"], "mutable": False, "input_type": a["type"],
                              "default_value": str(a.get("default", "")),
                              "values": [str(v) for v in a.get("values", [])] if a["type"] == "select" else []})
        # type "any": cho phép cả rectangle (detection) và polygon (segmentation) trong cùng Project
        labels.append({"name": name, "color": "#808080" if name == tax.ignore else COLORS[i % len(COLORS)],
                       "type": "any", "attributes": attrs})
    text = json.dumps(labels, ensure_ascii=False, indent=2)
    out = ROOT / "cvat" / "labels_generated.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text + "\n", encoding="utf8")
    print(f"Đã ghi {rel(out)} (taxonomy {tax.version}, {len(labels)} nhãn). "
          "Dán nội dung vào CVAT: Project -> Labels -> Raw -> Done.")


if __name__ == "__main__":
    main()
