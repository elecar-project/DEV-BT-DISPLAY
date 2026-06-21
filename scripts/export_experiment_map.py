#!/usr/bin/env python3
"""Export the confirmed draw.io experiment map as a static SVG for GitHub Pages."""

from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path


SOURCE = Path("/workspaces/Dev-BT/實存圖.drawio")
OUTPUT = Path(__file__).resolve().parents[1] / "docs/assets/img/experiment-map-full.svg"
LINKS = {
    "A03：min_cluster_size": "../../results/a03-min-cluster-overview.html",
    "A04：UMAP": "../../results/a04-umap-overview.html",
    "A05：停用詞": "../../results/a05-stopwords-overview.html",
    "2 (del)_tok": "../../results/a03-2-del-tok.html",
    "3 (del)_tok(para12-80)": "../../results/a03-3-del-tok-para12-80.html",
    "5 (repl)_tok": "../../results/a03-5-repl-tok.html",
    "5.1 (repl-y)_tok": "../../results/a03-5-1-repl-y-tok.html",
    "6 (repl)_tok(para12-80)": "../../results/a03-6-repl-tok-para12-80.html",
    "6.1 (repl-y)_tok(para12-80)": "../../results/a03-6-1-repl-y-tok-para12-80.html",
    "7 (orig)_tok": "../../results/a03-7-orig-tok.html",
    "8 (orig)_tok(para12-80)": "../../results/a03-8-orig-tok-para12-80.html",
    "2020 前 (08-19)": "../../results/b01-08-19-min-cluster.html",
    "2020 後 (20-25)": "../../results/b01-20-25-min-cluster.html",
    "8New-LLM30": "../../results/m02-llm30.html",
    "8New-LLM50": "../../results/m02-llm50.html",
    "2020 前": "../../results/m03-2020-before.html",
}
NODE_LINKS = {
    "mRq0KLDsOoRAvhbJz9B0-46": "../../results/m01-8-historical.html",
    "mRq0KLDsOoRAvhbJz9B0-69": "../../results/m01-8-historical.html",
    "mRq0KLDsOoRAvhbJz9B0-19": "../../results/a04-2-del-tok.html",
    "mRq0KLDsOoRAvhbJz9B0-21": "../../results/a04-3-del-tok-para12-80.html",
    "mRq0KLDsOoRAvhbJz9B0-27": "../../results/a04-5-repl-tok.html",
    "mRq0KLDsOoRAvhbJz9B0-23": "../../results/a04-6-repl-tok-para12-80.html",
    "mRq0KLDsOoRAvhbJz9B0-24": "../../results/a04-7-orig-tok.html",
    "mRq0KLDsOoRAvhbJz9B0-26": "../../results/a04-8-orig-tok-para12-80.html",
    "mRq0KLDsOoRAvhbJz9B0-75": "../../results/a04-b01-08-19.html",
    "mRq0KLDsOoRAvhbJz9B0-80": "../../results/a04-b01-20-25.html",
    "mRq0KLDsOoRAvhbJz9B0-82": "../../results/m03-2020-after.html",
    "mRq0KLDsOoRAvhbJz9B0-84": "../../results/t01-overview.html",
    "mRq0KLDsOoRAvhbJz9B0-85": "../../results/t01-del.html",
    "mRq0KLDsOoRAvhbJz9B0-86": "../../results/t01-repl.html",
    "mRq0KLDsOoRAvhbJz9B0-88": "../../results/t02-overview.html",
    "mRq0KLDsOoRAvhbJz9B0-89": "../../results/t02-2018-before.html",
    "mRq0KLDsOoRAvhbJz9B0-90": "../../results/t02-2018-after.html",
    "mRq0KLDsOoRAvhbJz9B0-91": "../../results/t02-2019-after.html",
    "mRq0KLDsOoRAvhbJz9B0-92": "../../results/t02-2019-before.html",
    "mRq0KLDsOoRAvhbJz9B0-93": "../../results/t02-2021-before.html",
    "mRq0KLDsOoRAvhbJz9B0-94": "../../results/t02-2021-after.html",
    "mRq0KLDsOoRAvhbJz9B0-29": "../../results/a05-6-overview.html",
    "mRq0KLDsOoRAvhbJz9B0-45": "../../results/a05-8-orig-rev-overview.html",
}
EMPTY_NODE_LABELS = {
    "1 (del)", "4 (repl)", "0 (orig)", "8C", "2020 後",
    "2018 前 (08-17)", "2018 後 (18-25)", "2019 前 (08-18)",
    "2019 後 (19-25)", "2021 前 (08-20)", "2021 後 (21-25)",
    "2018 前", "2018 後", "2019 前", "2019 後", "2021 前", "2021 後",
    "8 (orig)_tok(para12-80)_影長1~35m", "8 (orig)_tok(para12-80)_去頭尾5廠",
    "8New-影長1~35m", "8New-去頭尾5廠",
}


def style_value(style: str, name: str, default: str = "") -> str:
    match = re.search(rf"(?:^|;){re.escape(name)}=([^;]+)", style)
    value = match.group(1) if match else default
    light_dark = re.match(r"light-dark\((#[0-9a-fA-F]{3,8})\s*,", value)
    return light_dark.group(1) if light_dark else value


def label(value: str) -> str:
    text = html.unescape(value or "")
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</?(?:div|span)[^>]*>", "", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text).strip()
    if text.startswith(("M0", "T0")) and "（" in text:
        text = text.replace("（", "\n（", 1)
    return text


def point(node: dict, x_ratio: float, y_ratio: float) -> tuple[float, float]:
    return node["x"] + node["w"] * x_ratio, node["y"] + node["h"] * y_ratio


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def text_width(value: str, font_size: float) -> float:
    return sum(font_size * (0.96 if ord(char) > 127 else 0.68) for char in value)


def text_lines(value: str, width: float, font_size: float) -> list[str]:
    explicit = value.splitlines()
    lines: list[str] = []
    for part in explicit:
        current = ""
        for char in part:
            if current and text_width(current + char, font_size) > width:
                lines.append(current)
                current = char
            else:
                current += char
        part = current
        lines.append(part)
    return lines or [""]


def fitted_text(value: str, width: float, height: float, preferred: float) -> tuple[float, list[str]]:
    font_size = preferred
    while font_size > 10:
        lines = text_lines(value, width, font_size)
        if len(lines) * font_size * 1.16 <= height - 5:
            return font_size, lines
        font_size -= 0.5
    return font_size, text_lines(value, width, font_size)


def orthogonal_points(
    start: tuple[float, float], end: tuple[float, float], anchors: list[tuple[float, float]]
) -> list[tuple[float, float]]:
    points = [start]
    current = start
    for anchor in anchors:
        if current[0] != anchor[0] and current[1] != anchor[1]:
            points.append((anchor[0], current[1]))
        points.append(anchor)
        current = anchor
    if not anchors and current[0] != end[0] and current[1] != end[1]:
        midpoint = (current[0] + end[0]) / 2
        points.extend([(midpoint, current[1]), (midpoint, end[1])])
    elif current[0] != end[0] and current[1] != end[1]:
        points.append((current[0], end[1]))
    points.append(end)
    return points


def main() -> None:
    root = ET.parse(SOURCE).getroot()
    model = root.find(".//mxGraphModel")
    if model is None:
        raise RuntimeError("mxGraphModel not found")

    cells = model.findall("./root/mxCell")
    nodes: dict[str, dict] = {}
    for cell in cells:
        if cell.get("vertex") != "1":
            continue
        geometry = cell.find("mxGeometry")
        if geometry is None:
            continue
        style = cell.get("style", "")
        nodes[cell.get("id", "")] = {
            "id": cell.get("id", ""),
            "label": label(cell.get("value", "")),
            "x": float(geometry.get("x", "0")),
            "y": float(geometry.get("y", "0")),
            "w": float(geometry.get("width", "110")),
            "h": float(geometry.get("height", "32")),
            "fill": style_value(style, "fillColor", "#ffffff"),
            "stroke": style_value(style, "strokeColor", "#6b7280"),
            "font": float(style_value(style, "fontSize", "14")),
            "font_color": style_value(style, "fontColor", "#1f2937"),
        }

    edge_paths: list[str] = []
    seen_connections: set[tuple[str, str]] = set()
    for cell in cells:
        if cell.get("edge") != "1":
            continue
        source = nodes.get(cell.get("source", ""))
        target = nodes.get(cell.get("target", ""))
        if not source or not target:
            continue
        connection = (source["id"], target["id"])
        if connection in seen_connections:
            continue
        seen_connections.add(connection)
        style = cell.get("style", "")
        exit_x = float(style_value(style, "exitX", "1"))
        exit_y = float(style_value(style, "exitY", "0.5"))
        entry_x = float(style_value(style, "entryX", "0"))
        entry_y = float(style_value(style, "entryY", "0.5"))
        start = point(source, exit_x, exit_y)
        end = point(target, entry_x, entry_y)
        anchors: list[tuple[float, float]] = []
        geometry = cell.find("mxGeometry")
        if geometry is not None:
            for item in geometry.findall(".//mxPoint"):
                anchors.append((float(item.get("x", "0")), float(item.get("y", "0"))))
        # The confirmed map routes T02/T03 validation branches through an open
        # vertical lane before M01, rather than behind the downstream results.
        if source["id"].endswith("-45") and target["id"].endswith(("-49", "-50")):
            anchors = [(615.0, start[1]), (615.0, end[1])]
        elif source["id"].endswith("-45") and target["id"].endswith(("-81", "-82")):
            anchors = [(550.0, start[1]), (550.0, end[1])]
        elif source["id"].endswith("-45") and target["id"].endswith(("-89", "-90", "-91", "-92", "-93", "-94")):
            anchors = [(575.0, start[1]), (575.0, end[1])]
        elif source["id"].endswith("-45") and target["id"].endswith(("-96", "-97")):
            anchors = [(600.0, start[1]), (600.0, end[1])]
        # Draw.io stores a few one-digit routing nudges. Keeping them creates
        # visible hooks in SVG, so collapse them onto the outgoing horizontal.
        if anchors and abs(anchors[0][1] - start[1]) < 16:
            anchors[0] = (anchors[0][0], start[1])
        points = orthogonal_points(start, end, anchors)
        d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in points)
        color = style_value(style, "strokeColor", "#475569")
        edge_paths.append(
            f'<path d="{d}" class="edge" data-source="{escape(source["id"])}" '
            f'data-target="{escape(target["id"])}" data-color="{escape(color)}" marker-end="url(#arrow)"/>'
        )

    node_shapes: list[str] = []
    for node in nodes.values():
        safe_label = escape(node["label"])
        # A03 is the source-dataset column. Its variable-width boxes read more
        # cleanly when every dataset number begins at the same left inset.
        left_aligned = node["x"] == 47 and node["y"] < 550
        classes = "node dataset-node" if left_aligned else "node"
        href = NODE_LINKS.get(node["id"]) or LINKS.get(node["label"])
        if node["label"] in EMPTY_NODE_LABELS and not href:
            classes += " is-empty"
        font_size, lines = fitted_text(node["label"], node["w"] - 12, node["h"], node["font"])
        line_height = font_size * 1.16
        text_y = node["y"] + (node["h"] - line_height * len(lines)) / 2 + font_size
        text_x = node["x"] + 18 if left_aligned else node["x"] + node["w"] / 2
        tspans = "".join(
            f'<tspan x="{text_x:.1f}" dy="{0 if index == 0 else line_height:.1f}">{escape(line)}</tspan>'
            for index, line in enumerate(lines)
        )
        shape = (
            f'<g class="{classes}" data-id="{escape(node["id"])}" data-label="{safe_label}">'
            f'<rect x="{node["x"]:.1f}" y="{node["y"]:.1f}" width="{node["w"]:.1f}" height="{node["h"]:.1f}" '
            f'fill="{escape(node["fill"])}" stroke="{escape(node["stroke"])}"/>'
            f'<text x="{text_x:.1f}" y="{text_y:.1f}" fill="{escape(node["font_color"])}" '
            f'font-size="{font_size:.1f}">{tspans}</text></g>'
        )
        # The map is embedded with <object>. _top prevents linked result pages
        # from rendering inside the map's own viewport.
        node_shapes.append(f'<a href="{escape(href)}" target="_top">{shape}</a>' if href else shape)

    interaction_script = '''<script><![CDATA[
    const edges = Array.from(document.querySelectorAll('.edge'));
    const incoming = new Map();
    edges.forEach((edge) => {
      const key = edge.dataset.target;
      incoming.set(key, [...(incoming.get(key) || []), edge]);
    });
    function clear() {
      edges.forEach((edge) => { edge.classList.remove('active'); edge.style.stroke = ''; });
    }
    function highlight(nodeId) {
      clear();
      const seen = new Set();
      function visit(id) {
        (incoming.get(id) || []).forEach((edge) => {
          if (seen.has(edge)) return;
          seen.add(edge);
          edge.classList.add('active');
          edge.style.stroke = edge.dataset.color;
          visit(edge.dataset.source);
        });
      }
      visit(nodeId);
    }
    document.querySelectorAll('.node').forEach((node) => {
      node.addEventListener('mouseenter', () => highlight(node.dataset.id));
      node.addEventListener('mouseleave', clear);
    });
  ]]></script>'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1654 1169" role="img" aria-label="DEV-BT 完整實驗運行架構圖">
  <style>
    .edge {{ fill: none; stroke: #a8b1c1; stroke-width: 1.5; stroke-linejoin: round; stroke-linecap: round; }}
    .edge.active {{ stroke-width: 2.4; stroke-dasharray: 7 5; animation: flow 0.9s linear infinite; }}
    .node rect {{ stroke-width: 1.1; }}
    .node text {{ font-family: "Noto Serif TC", "PMingLiU", serif; text-anchor: middle; dominant-baseline: alphabetic; }}
    .dataset-node text {{ text-anchor: start; }}
    .node.is-empty {{ filter: grayscale(1); opacity: 0.58; }}
    a .node:hover rect {{ stroke: #0f766e; stroke-width: 3; }}
    a .node:hover text {{ fill: #0f766e; font-weight: 700; }}
    .node:hover rect {{ stroke-width: 2.6; }}
    @keyframes flow {{ to {{ stroke-dashoffset: -12; }} }}
  </style>
  <defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="context-stroke"/></marker></defs>
  {''.join(edge_paths)}
  {''.join(node_shapes)}
  {interaction_script}
</svg>'''
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(nodes)} nodes and {len(edge_paths)} edges")


if __name__ == "__main__":
    main()
