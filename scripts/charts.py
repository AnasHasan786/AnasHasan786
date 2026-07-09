"""
charts.py
----------
Pure-Python SVG chart generation. Every function takes plain data (as
produced by github_api.build_dashboard_data) and returns a complete,
standalone SVG document string, ready to be written straight to disk.

Design language (applies to every chart):
  * background  #0D1117   card #161B22   border #30363D
  * accent blues only (#00BFFF / #38BDF8 and the BLUE_SHADES ramp)
  * 12px card radius, thin 1px borders, generous internal padding
  * grid lines are a faint #21262D so they recede behind the data
"""

from __future__ import annotations

import datetime as _dt

from utils import (
    COLORS,
    BLUE_SHADES,
    FONT_STACK,
    RADIUS,
    format_number,
    linear_gradient,
    month_short_name,
    render_card,
    rounded_rect,
    smooth_path,
    text,
)

# Icons are tiny inline stroke-icons (Feather/Lucide-style), drawn directly
# in the accent color so they read cleanly at small sizes.
_ICONS = {
    "commits": (
        '<circle cx="10" cy="10" r="3.2" fill="none" stroke="{c}" stroke-width="1.6"/>'
        '<line x1="10" y1="0.5" x2="10" y2="6.8" stroke="{c}" stroke-width="1.6"/>'
        '<line x1="10" y1="13.2" x2="10" y2="19.5" stroke="{c}" stroke-width="1.6"/>'
    ),
    "repo": (
        '<rect x="1" y="2" width="18" height="16" rx="2.5" fill="none" stroke="{c}" stroke-width="1.6"/>'
        '<line x1="6" y1="2" x2="6" y2="18" stroke="{c}" stroke-width="1.6"/>'
    ),
    "star": (
        '<path d="M10 1.5 L12.3 7.1 L18.3 7.6 L13.7 11.5 L15.1 17.4 L10 14.1 '
        'L4.9 17.4 L6.3 11.5 L1.7 7.6 L7.7 7.1 Z" fill="{c}" opacity="0.9"/>'
    ),
    "pr": (
        '<circle cx="5" cy="4" r="2.1" fill="none" stroke="{c}" stroke-width="1.6"/>'
        '<circle cx="5" cy="16" r="2.1" fill="none" stroke="{c}" stroke-width="1.6"/>'
        '<circle cx="15" cy="10" r="2.1" fill="none" stroke="{c}" stroke-width="1.6"/>'
        '<path d="M5 6.1 V13.9" stroke="{c}" stroke-width="1.6" fill="none"/>'
        '<path d="M5 6.1 Q5 10 15 10 V7.9" stroke="{c}" stroke-width="1.6" fill="none"/>'
    ),
    "followers": (
        '<circle cx="7" cy="6.5" r="3" fill="none" stroke="{c}" stroke-width="1.6"/>'
        '<path d="M1.5 18 Q1.5 12.5 7 12.5 Q12.5 12.5 12.5 18" fill="none" stroke="{c}" stroke-width="1.6"/>'
        '<circle cx="15.5" cy="7.5" r="2.3" fill="none" stroke="{c}" stroke-width="1.4" opacity="0.65"/>'
    ),
    "following": (
        '<circle cx="7" cy="6.5" r="3" fill="none" stroke="{c}" stroke-width="1.6"/>'
        '<path d="M1.5 18 Q1.5 12.5 7 12.5 Q12.5 12.5 12.5 18" fill="none" stroke="{c}" stroke-width="1.6"/>'
        '<path d="M15 5.5 V10.5 M12.7 8 H17.3" stroke="{c}" stroke-width="1.5"/>'
    ),
    "contributed": (
        '<rect x="1" y="1" width="7" height="7" rx="1.6" fill="{c}" opacity="0.9"/>'
        '<rect x="11" y="1" width="7" height="7" rx="1.6" fill="{c}" opacity="0.45"/>'
        '<rect x="1" y="11" width="7" height="7" rx="1.6" fill="{c}" opacity="0.45"/>'
        '<rect x="11" y="11" width="7" height="7" rx="1.6" fill="{c}" opacity="0.9"/>'
    ),
}


def _icon(name: str, color: str) -> str:
    return f'<svg width="20" height="20" viewBox="0 0 20 20">{_ICONS[name].format(c=color)}</svg>'


# ----------------------------------------------------------------------------
# 1. KPI cards
# ----------------------------------------------------------------------------
def generate_kpi_cards(data: dict) -> str:
    profile = data["profile"]
    metrics = [
        ("commits", "Total Commits", profile["total_commit_contributions"], "Last 12 months"),
        ("repo", "Repositories", profile["public_repos"], "Public, non-fork"),
        ("star", "Stars Earned", data["stars"], "Across all repos"),
        ("pr", "Pull Requests", data["pull_requests"], "All-time, all repos"),
        ("followers", "Followers", profile["followers"], "GitHub community"),
        ("following", "Following", profile["following"], "Developers followed"),
        ("contributed", "Contributed Repos", profile["contributed_repos"], "Commits last 12 months"),
    ]

    cols, gap, margin = 4, 16, 24
    width = 960
    card_w = (width - 2 * margin - (cols - 1) * gap) / cols
    card_h = 116
    row_gap = 16
    rows = -(-len(metrics) // cols)  # ceil
    height = margin * 2 + rows * card_h + (rows - 1) * row_gap + 40  # +40 header

    parts = [
        rounded_rect(0.5, 0.5, width - 1, height - 1, RADIUS, COLORS["bg"], COLORS["border"], 1),
        text(margin, 34, "Overview", size=15, color=COLORS["text"], weight=600),
        text(margin, 52, "Key profile metrics, refreshed nightly", size=11.5, color=COLORS["subtext"]),
    ]

    top_offset = 68
    for i, (icon_name, label, value, desc) in enumerate(metrics):
        row, col = divmod(i, cols)
        x = margin + col * (card_w + gap)
        y = top_offset + row * (card_h + row_gap)

        parts.append(rounded_rect(x, y, card_w, card_h, RADIUS, COLORS["card"], COLORS["border"], 1))
        # accent chip behind icon
        parts.append(
            f'<rect x="{x + 16}" y="{y + 16}" width="36" height="36" rx="9" '
            f'fill="{COLORS["primary"]}" opacity="0.12" />'
        )
        parts.append(f'<g transform="translate({x + 24}, {y + 24})">{_ICONS[icon_name].format(c=COLORS["primary"])}</g>')

        parts.append(text(x + card_w - 16, y + 38, format_number(value), size=24, color=COLORS["text"], weight=700, anchor="end"))
        parts.append(text(x + 16, y + 74, label, size=12.5, color=COLORS["text"], weight=600))
        parts.append(text(x + 16, y + 92, desc, size=10.5, color=COLORS["subtext"], weight=400))

    svg_body = "\n".join(parts)
    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'fill="none" xmlns="http://www.w3.org/2000/svg">\n{svg_body}\n</svg>'
    )


# ----------------------------------------------------------------------------
# shared chart-plot geometry helper
# ----------------------------------------------------------------------------
def _plot_frame(width, height, pad_left=44, pad_right=24, pad_top=70, pad_bottom=36):
    return {
        "x0": pad_left,
        "x1": width - pad_right,
        "y0": pad_top,
        "y1": height - pad_bottom,
        "w": width - pad_left - pad_right,
        "h": height - pad_top - pad_bottom,
    }


def _grid_lines(frame, rows=4):
    parts = []
    for i in range(rows + 1):
        y = frame["y0"] + frame["h"] * i / rows
        parts.append(
            f'<line x1="{frame["x0"]}" y1="{y:.2f}" x2="{frame["x1"]}" y2="{y:.2f}" '
            f'stroke="{COLORS["grid"]}" stroke-width="1" />'
        )
    return "\n".join(parts)


# ----------------------------------------------------------------------------
# 2. Weekly activity — smooth line chart
# ----------------------------------------------------------------------------
def generate_weekly_activity_chart(weekly_activity: list[dict]) -> str:
    width, height = 460, 300
    frame = _plot_frame(width, height)
    values = [w["commits"] for w in weekly_activity] or [0]
    max_val = max(values) or 1
    max_val = max_val * 1.15  # headroom

    n = len(weekly_activity)
    points = []
    for i, w in enumerate(weekly_activity):
        x = frame["x0"] + (frame["w"] * i / max(n - 1, 1))
        y = frame["y1"] - (w["commits"] / max_val) * frame["h"]
        points.append((x, y))

    path_d = smooth_path(points) if len(points) > 1 else ""

    defs = linear_gradient(
        "lineStroke", frame["x0"], 0, frame["x1"], 0,
        [(0, COLORS["secondary"], 1), (100, COLORS["primary"], 1)],
    )
    dot_fill = COLORS["primary"]

    inner = [f"<defs>{defs}</defs>", _grid_lines(frame)]

    # y-axis labels
    for i in range(5):
        val = max_val * (4 - i) / 4
        y = frame["y0"] + frame["h"] * i / 4
        inner.append(text(frame["x0"] - 10, y + 4, format_number(round(val)), size=10, color=COLORS["subtext"], anchor="end"))

    if path_d:
        inner.append(f'<path d="{path_d}" fill="none" stroke="url(#lineStroke)" stroke-width="2.5" stroke-linecap="round" />')
        for (x, y) in points:
            inner.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.2" fill="{COLORS["bg"]}" stroke="{dot_fill}" stroke-width="2" />')

    # x-axis labels (every other week to avoid crowding)
    for i, w in enumerate(weekly_activity):
        if i % 2 != 0 and n > 8:
            continue
        x = frame["x0"] + (frame["w"] * i / max(n - 1, 1))
        try:
            d = _dt.datetime.strptime(w["week_start"], "%Y-%m-%d")
            label = f"{month_short_name(d.month)} {d.day}"
        except Exception:
            label = ""
        inner.append(text(x, height - 14, label, size=9.5, color=COLORS["subtext"], anchor="middle"))

    inner_svg = "\n".join(inner)
    return render_card(
        title="Weekly Activity",
        subtitle="Commits per week · last 12 weeks",
        width=width,
        height=height,
        inner_svg=inner_svg,
    )


# ----------------------------------------------------------------------------
# 3. Commit trend — area chart (cumulative)
# ----------------------------------------------------------------------------
def generate_commit_trend_chart(commit_trend: list[dict]) -> str:
    width, height = 460, 300
    frame = _plot_frame(width, height)
    values = [c["cumulative"] for c in commit_trend] or [0]
    max_val = (max(values) or 1) * 1.1

    n = len(commit_trend)
    points = []
    for i, c in enumerate(commit_trend):
        x = frame["x0"] + (frame["w"] * i / max(n - 1, 1))
        y = frame["y1"] - (c["cumulative"] / max_val) * frame["h"]
        points.append((x, y))

    path_d = smooth_path(points) if len(points) > 1 else ""
    area_d = ""
    if path_d:
        area_d = path_d + f" L {points[-1][0]:.2f} {frame['y1']:.2f} L {points[0][0]:.2f} {frame['y1']:.2f} Z"

    defs = (
        linear_gradient(
            "areaFill", 0, frame["y0"], 0, frame["y1"],
            [(0, COLORS["primary"], 0.35), (100, COLORS["primary"], 0.02)],
        )
        + linear_gradient(
            "areaStroke", frame["x0"], 0, frame["x1"], 0,
            [(0, COLORS["secondary"], 1), (100, COLORS["primary"], 1)],
        )
    )

    inner = [f"<defs>{defs}</defs>", _grid_lines(frame)]

    for i in range(5):
        val = max_val * (4 - i) / 4
        y = frame["y0"] + frame["h"] * i / 4
        inner.append(text(frame["x0"] - 10, y + 4, format_number(round(val)), size=10, color=COLORS["subtext"], anchor="end"))

    if area_d:
        inner.append(f'<path d="{area_d}" fill="url(#areaFill)" stroke="none" />')
        inner.append(f'<path d="{path_d}" fill="none" stroke="url(#areaStroke)" stroke-width="2.5" stroke-linecap="round" />')

    for i, c in enumerate(commit_trend):
        if i % 2 != 0 and n > 8:
            continue
        x = frame["x0"] + (frame["w"] * i / max(n - 1, 1))
        try:
            d = _dt.datetime.strptime(c["week_start"], "%Y-%m-%d")
            label = f"{month_short_name(d.month)} {d.day}"
        except Exception:
            label = ""
        inner.append(text(x, height - 14, label, size=9.5, color=COLORS["subtext"], anchor="middle"))

    inner_svg = "\n".join(inner)
    return render_card(
        title="Commit Trend",
        subtitle="Cumulative commits · last 12 weeks",
        width=width,
        height=height,
        inner_svg=inner_svg,
    )


# ----------------------------------------------------------------------------
# 4. Repository growth — rounded bar chart
# ----------------------------------------------------------------------------
def generate_repo_growth_chart(repo_growth: list[dict]) -> str:
    width, height = 460, 300
    frame = _plot_frame(width, height)
    values = [r["count"] for r in repo_growth] or [0]
    max_val = (max(values) or 1) * 1.15

    n = len(repo_growth)
    bar_gap = 10
    bar_w = (frame["w"] - bar_gap * (n - 1)) / n if n else frame["w"]

    defs = linear_gradient(
        "barFill", 0, frame["y0"], 0, frame["y1"],
        [(0, COLORS["secondary"], 1), (100, COLORS["primary"], 0.55)],
    )

    inner = [f"<defs>{defs}</defs>", _grid_lines(frame)]

    for i in range(5):
        val = max_val * (4 - i) / 4
        y = frame["y0"] + frame["h"] * i / 4
        inner.append(text(frame["x0"] - 10, y + 4, format_number(round(val)), size=10, color=COLORS["subtext"], anchor="end"))

    for i, r in enumerate(repo_growth):
        x = frame["x0"] + i * (bar_w + bar_gap)
        bar_h = (r["count"] / max_val) * frame["h"]
        y = frame["y1"] - bar_h
        radius = min(6, bar_w / 2)
        inner.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_w:.2f}" height="{max(bar_h, 2):.2f}" '
            f'rx="{radius:.2f}" ry="{radius:.2f}" fill="url(#barFill)" />'
        )
        if n <= 12:
            label = month_short_name(r["month"])
            inner.append(text(x + bar_w / 2, height - 14, label, size=9.5, color=COLORS["subtext"], anchor="middle"))

    inner_svg = "\n".join(inner)
    return render_card(
        title="Repository Growth",
        subtitle="Cumulative public repos · last 12 months",
        width=width,
        height=height,
        inner_svg=inner_svg,
    )


# ----------------------------------------------------------------------------
# 5. Language distribution — donut chart (blue shades only)
# ----------------------------------------------------------------------------
def generate_language_distribution_chart(languages: list[dict]) -> str:
    width, height = 460, 300
    cx, cy, r_outer, r_inner = 128, 178, 82, 52

    total = sum(l["count"] for l in languages) or 1
    inner = []
    start_angle = -90.0

    def polar(cx, cy, r, angle_deg):
        angle_rad = (angle_deg * 3.14159265) / 180
        return cx + r * __import__("math").cos(angle_rad), cy + r * __import__("math").sin(angle_rad)

    if not languages:
        inner.append(
            text(cx, cy, "No language data", size=12, color=COLORS["subtext"], anchor="middle")
        )
    else:
        for i, lang in enumerate(languages):
            fraction = lang["count"] / total
            sweep = fraction * 360
            end_angle = start_angle + sweep
            large_arc = 1 if sweep > 180 else 0
            color = BLUE_SHADES[i % len(BLUE_SHADES)]

            x0, y0 = polar(cx, cy, r_outer, start_angle)
            x1, y1 = polar(cx, cy, r_outer, end_angle)
            xi1, yi1 = polar(cx, cy, r_inner, end_angle)
            xi0, yi0 = polar(cx, cy, r_inner, start_angle)

            path = (
                f"M {x0:.2f} {y0:.2f} "
                f"A {r_outer} {r_outer} 0 {large_arc} 1 {x1:.2f} {y1:.2f} "
                f"L {xi1:.2f} {yi1:.2f} "
                f"A {r_inner} {r_inner} 0 {large_arc} 0 {xi0:.2f} {yi0:.2f} Z"
            )
            inner.append(f'<path d="{path}" fill="{color}" opacity="0.95" />')
            start_angle = end_angle

        inner.append(text(cx, cy - 4, format_number(total), size=22, color=COLORS["text"], weight=700, anchor="middle"))
        inner.append(text(cx, cy + 16, "repos analyzed", size=10.5, color=COLORS["subtext"], anchor="middle"))

    # legend
    legend_x = 250
    legend_y = 92
    row_h = 26
    for i, lang in enumerate(languages[:7]):
        color = BLUE_SHADES[i % len(BLUE_SHADES)]
        y = legend_y + i * row_h
        inner.append(f'<circle cx="{legend_x}" cy="{y}" r="5" fill="{color}" />')
        inner.append(text(legend_x + 14, y + 4, lang["language"], size=12, color=COLORS["text"], weight=500))
        inner.append(text(width - 24, y + 4, f'{lang["pct"]}%', size=12, color=COLORS["subtext"], anchor="end"))

    inner_svg = "\n".join(inner)
    return render_card(
        title="Language Distribution",
        subtitle="By repository, primary language",
        width=width,
        height=height,
        inner_svg=inner_svg,
    )
