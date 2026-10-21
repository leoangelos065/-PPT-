#!/usr/bin/env python3
"""Read-only PPTX structure inventory; visual verification remains mandatory."""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main"}


def inspect(path: Path) -> dict:
    report = {"status": "pass", "slides": [], "issues": [],
              "limitations": ["Declared fonts are not proof of installed or rendered fonts.",
                              "No rendered overflow, pixel fidelity or optical alignment test."]}
    with zipfile.ZipFile(path) as package:
        invalid = package.testzip()
        if invalid:
            report["issues"].append({"kind": "invalid_zip_member", "file": invalid})
        pres = ET.fromstring(package.read("ppt/presentation.xml"))
        size = pres.find("p:sldSz", NS)
        report["slide_size_emu"] = {k: int(size.get(k, "0")) for k in ("cx", "cy")} if size is not None else None
        paths = sorted((n for n in package.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
                       key=lambda n: int(re.search(r"slide(\d+)\.xml", n).group(1)))
        for name in paths:
            root = ET.fromstring(package.read(name))
            entries = []
            ids = set()
            for element in root.iter():
                if element.tag not in {f"{{{NS['p']}}}{t}" for t in ("sp", "pic", "grpSp", "graphicFrame", "cxnSp")}:
                    continue
                props = next((c for child in element for c in child if c.tag == f"{{{NS['p']}}}cNvPr"), None)
                if props is None:
                    continue
                obj_id = props.get("id")
                if obj_id in ids:
                    report["issues"].append({"kind": "duplicate_object_id", "slide": name, "id": obj_id})
                ids.add(obj_id)
                is_group = element.tag.endswith("}grpSp")
                frame = element.find("p:txBody", NS)
                lines = []  # Text comes only from a:t, not XML indentation.
                if frame is not None:
                    lines = ["".join(n.text or "" for n in p.findall(".//a:t", NS)) for p in frame.findall("a:p", NS)]
                fonts = sorted({f.get("typeface") for f in frame.iter() if f.tag in {f"{{{NS['a']}}}{t}" for t in ("latin", "ea", "cs")} and f.get("typeface")}) if frame is not None else []
                entry = {"id": obj_id, "name": props.get("name", ""), "type": element.tag.split("}")[-1], "text": "\n".join(lines), "fonts": fonts}
                xform = element.find("p:spPr/a:xfrm", NS)
                if xform is not None:
                    off, ext = xform.find("a:off", NS), xform.find("a:ext", NS)
                    if off is not None and ext is not None:
                        entry["geometry_emu"] = {k: int(node.get(k, "0")) for node, keys in ((off, ("x", "y")), (ext, ("cx", "cy"))) for k in keys}
                        if any(entry["geometry_emu"][k] < 0 for k in ("cx", "cy")):
                            report["issues"].append({"kind": "negative_extent", "slide": name, "object": entry["name"]})
                if not is_group and entry["text"] and not fonts:
                    entry["font_note"] = "No explicit face found; inspect theme/inheritance in the renderer."
                entries.append(entry)
            report["slides"].append({"file": name, "objects_including_group_children": entries,
                                     "normal_text_objects": sum(bool(e["text"].strip()) for e in entries)})
        for info in package.infolist():
            if info.filename.startswith("ppt/media/") and not info.is_dir() and info.file_size == 0:
                report["issues"].append({"kind": "empty_media", "file": info.filename})
    if report["issues"]:
        report["status"] = "fail"
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pptx", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    if args.pptx.resolve() == args.report.resolve():
        parser.error("The report path must not overwrite the input PPTX.")
    try:
        report = inspect(args.pptx)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, ET.ParseError) as error:
        report = {"status": "fail", "issues": [{"kind": "unreadable_package", "detail": str(error)}]}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": report["status"], "issues": len(report["issues"]), "report": str(args.report)}, ensure_ascii=False))
    return 1 if report["issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
