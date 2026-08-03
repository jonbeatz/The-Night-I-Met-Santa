"""Shared helpers for PS → InDesign type inventory (TNIMS + Hermes picture books)."""
from __future__ import annotations

import re
from typing import Any

DPI_DEFAULT = 300.0
BLEED_IN_DEFAULT = 0.125

# PSB unit group name → Media/development folder (when present)
UNIT_DEV_FOLDERS = {
    "PO": "P0-Legal",
    "P0": "P0-Legal",
    "P01": "P01-title",
    "P02": "P02-about-spread",
    "S01": "S01-approach",
    "S02": "S02-threshold",
    "S03": "S03-eyes-met",
    "S04": "S04-sit-here",
    "S05": "S05-chat",
    "S06": "S06-cocoa",
    "S07": "S07-proof",
    "S08": "S08-gone",
    "S09": "S09-search",
    "S10": "S10-note",
    "S11": "S11-wish",
    "S12": "S12-god-bless",
    "P-author-thank-you": "P-thank-you",
    "P32-33-thank-you": "P-thank-you",
    "Back-Page": "P-quiet-close",
}

ALIGN_MAP = {
    0: "left",
    1: "right",
    2: "center",
    3: "justify",
    4: "justify",
    # StyleRunAlignment enum variants seen in engine_dict
    "left": "left",
    "right": "right",
    "center": "center",
    "justify": "justify",
    "justifyLeft": "justify",
    "justifyAll": "justify",
}


def jsafe(v: Any) -> Any:
    """psd_tools returns custom String/Integer wrappers — coerce for JSON."""
    if v is None or isinstance(v, (bool, int, float, str)):
        return v
    if isinstance(v, (list, tuple)):
        return [jsafe(x) for x in v]
    if isinstance(v, dict):
        return {str(k): jsafe(val) for k, val in v.items()}
    try:
        return float(v)
    except Exception:
        return str(v)


def type_text(layer) -> str:
    try:
        ed = layer.engine_dict
        if ed and "Editor" in ed:
            raw = ed["Editor"].get("Text", "")
            if isinstance(raw, bytes):
                raw = raw.decode("utf-16-be", errors="ignore")
            if raw:
                return str(raw).replace("\r", "\n").strip()
    except Exception:
        pass
    try:
        t = layer.text
        if t:
            return str(t).replace("\r", "\n").strip()
    except Exception:
        pass
    return (layer.name or "").strip()


def clean_text(raw: str) -> str:
    s = (raw or "").strip()
    if (s.startswith("'") and s.endswith("'")) or (
        s.startswith('"') and s.endswith('"')
    ):
        s = s[1:-1]
    s = s.replace("\\x03", "\n").replace("\\r", "\n").replace("\\n", "\n")
    s = s.replace("\x03", "\n").replace("\r", "\n")
    s = re.sub(r"\n{3,}", "\n\n", s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    return s.strip()


def fill_to_hex(values) -> str | None:
    """PS FillColor Values often [type, r, g, b] floats 0–1 (or CMYK)."""
    if not values:
        return None
    try:
        vals = [float(x) for x in list(values)]
    except Exception:
        return None
    if len(vals) >= 4 and vals[0] in (0, 1) and max(vals[1:4]) <= 1.01:
        r, g, b = vals[1], vals[2], vals[3]
        return "#{:02X}{:02X}{:02X}".format(
            int(round(r * 255)), int(round(g * 255)), int(round(b * 255))
        )
    if len(vals) == 3 and max(vals) <= 1.01:
        r, g, b = vals
        return "#{:02X}{:02X}{:02X}".format(
            int(round(r * 255)), int(round(g * 255)), int(round(b * 255))
        )
    return None


def align_from_style(ss: dict) -> str:
    raw = ss.get("StyleRunAlignment")
    if raw is None:
        return "center"
    if isinstance(raw, (int, float)):
        return ALIGN_MAP.get(int(raw), "center")
    key = str(raw).split(".")[-1]
    return ALIGN_MAP.get(key, ALIGN_MAP.get(str(raw), "center"))


def metrics_and_runs(layer, dpi: float = DPI_DEFAULT) -> dict:
    """Font metrics + optional character runs when StyleRun differs."""
    out: dict[str, Any] = {
        "font": None,
        "style": None,
        "size_pt": None,
        "leading_pt": None,
        "tracking": None,
        "align": "center",
        "color": None,
        "runs": [],
        "metrics_err": None,
    }
    try:
        ed = layer.engine_dict
        fonts = list(layer.resource_dict.get("FontSet", []) or [])
        sr = ed.get("StyleRun") or {}
        run_array = list(sr.get("RunArray") or [])
        run_lengths = list(sr.get("RunLengthArray") or [])

        def run_style(i: int) -> dict:
            return run_array[i]["StyleSheet"]["StyleSheetData"]

        if not run_array:
            raise ValueError("no StyleRun")

        ss0 = run_style(0)
        fi = int(ss0.get("Font", 0) or 0)
        fname = "?"
        fstyle = None
        if fonts and fi < len(fonts):
            fname = str(fonts[fi].get("Name") or "?")
            fstyle = fonts[fi].get("Style")
            if fstyle is not None:
                fstyle = str(fstyle)

        sx = sy = 1.0
        try:
            tr = layer.transform
            sx, sy = float(tr[0]), float(tr[3])
        except Exception:
            pass

        raw_size = float(ss0.get("FontSize") or 0)
        lead = ss0.get("Leading")
        lead_raw = float(lead) if lead is not None else None
        size_pt = (raw_size * 72.0 / dpi) * sx
        leading_pt = (
            (lead_raw * 72.0 / dpi) * sy if lead_raw is not None else None
        )

        out["font"] = fname
        out["style"] = fstyle
        out["size_pt"] = round(size_pt, 2)
        out["leading_pt"] = round(leading_pt, 2) if leading_pt is not None else None
        out["tracking"] = jsafe(ss0.get("Tracking"))
        out["align"] = align_from_style(ss0)
        out["color"] = fill_to_hex(ss0.get("FillColor", {}).get("Values"))
        out["faux_bold"] = bool(ss0.get("FauxBold"))
        out["scale_x"] = sx
        out["scale_y"] = sy
        out["size_raw"] = raw_size
        out["leading_raw"] = lead_raw

        # Character runs when weight/size/color change across the layer
        text = clean_text(type_text(layer))
        if len(run_array) > 1 and run_lengths and text:
            cursor = 0
            base_key = (
                int(ss0.get("Font", 0) or 0),
                float(ss0.get("FontSize") or 0),
                bool(ss0.get("FauxBold")),
                fill_to_hex(ss0.get("FillColor", {}).get("Values")),
            )
            for i, length in enumerate(run_lengths):
                try:
                    ln = int(length)
                except Exception:
                    ln = 0
                start, end = cursor, cursor + ln
                cursor = end
                if i >= len(run_array):
                    break
                ss = run_style(i)
                key = (
                    int(ss.get("Font", 0) or 0),
                    float(ss.get("FontSize") or 0),
                    bool(ss.get("FauxBold")),
                    fill_to_hex(ss.get("FillColor", {}).get("Values")),
                )
                if key == base_key:
                    continue
                # Map PS char indices onto cleaned text length (best-effort)
                end_c = min(end, len(text))
                start_c = min(start, end_c)
                if start_c >= end_c:
                    continue
                char_style = "Poem-Emph"
                if key[1] < base_key[1] * 0.92:
                    char_style = "Poem-Small"
                out["runs"].append(
                    {
                        "start": start_c,
                        "end": end_c,
                        "character_style": char_style,
                        "font_index": key[0],
                        "size_raw": key[1],
                        "faux_bold": key[2],
                        "color": key[3],
                    }
                )
    except Exception as e:
        out["metrics_err"] = str(e)
    return out


def bbox_side_and_page(
    bbox: list[float] | None, canvas_w: float
) -> tuple[str, list[float] | None]:
    if not bbox:
        return "unknown", None
    mid = canvas_w / 2.0
    cx = (bbox[0] + bbox[2]) / 2.0
    side = "left" if cx < mid else "right"
    if side == "right":
        local = [bbox[0] - mid, bbox[1], bbox[2] - mid, bbox[3]]
    else:
        local = list(bbox)
    return side, local


def px_box_to_page_inches(
    bbox_page: list[float],
    dpi: float = DPI_DEFAULT,
    bleed_in: float = BLEED_IN_DEFAULT,
) -> dict:
    """bbox [l,t,r,b] page pixels (bleed canvas) → ID geometricBounds inches."""
    l, t, r, b = bbox_page
    return {
        "top": round(t / dpi - bleed_in, 4),
        "left": round(l / dpi - bleed_in, 4),
        "bottom": round(b / dpi - bleed_in, 4),
        "right": round(r / dpi - bleed_in, 4),
    }


def guess_paragraph_style(group: str, layer_name: str, text: str) -> str:
    g = (group or "").lower()
    n = (layer_name or "").lower()
    t = (text or "").lower()
    if "thank" in g or "author" in g:
        if "god bless" in t or t.startswith("—") or t.startswith("-"):
            return "Matter-Signoff"
        return "Matter-Body"
    if "p01" in g or "title" in n:
        return "Title-Main"
    if "p02" in g or "dedication" in n or "for my family" in t:
        return "Matter-Body"
    if "back" in g:
        return "Matter-Body"
    return "Poem-Body"


def is_guide_layer(name: str) -> bool:
    n = (name or "").lower()
    return (
        n.startswith("guide/")
        or "glow-shell" in n
        or "glow shell" in n
        or n.endswith(" shell")
    )
