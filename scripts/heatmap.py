"""
heatmap.py
-----------
Generates a fully custom contribution-calendar heatmap — visually inspired
by GitHub's own graph, but drawn from scratch (never embeds GitHub's default
graph image) and re-themed to the dashboard's blue palette.

This is the one component that genuinely benefits from `svgwrite`: a large,
uniform grid of small rounded squares. Everything else in this project uses
hand-built SVG strings for precise control over gradients/paths, but here
`svgwrite.Drawing` keeps the repeated-element loop clean and readable.
"""

from __future__ import annotations

import datetime as _dt

import svgwrite

from utils import COLORS, FONT_STACK, RADIUS, month_short_name, weekday_short_name


# Five-step intensity ramp, all within the blue family (no GitHub green).
_INTENSITY_COLORS = [
    COLORS["grid"],     # 0 contributions
    "#0C4A6E",
    "#0369A1",
    "#0EA5E9",
    "#00BFFF",           # highest activity
]


def _bucket_color(count: int, max_count: int) -> str:
    if count <= 0 or max_count <= 0:
        return _INTENSITY_COLORS[0]
    ratio = count / max_count
    if ratio > 0.75:
        return _INTENSITY_COLORS[4]
    if ratio > 0.5:
        return _INTENSITY_COLORS[3]
    if ratio > 0.25:
        return _INTENSITY_COLORS[2]
    return _INTENSITY_COLORS[1]


def generate_contribution_calendar(calendar_weeks: list[dict]) -> str:
    cell = 11
    gap = 3
    left_pad = 44
    top_pad = 72
    n_weeks = len(calendar_weeks)

    width = left_pad + n_weeks * (cell + gap) + 20
    height = top_pad + 7 * (cell + gap) + 50

    dwg = svgwrite.Drawing(size=(width, height))

    # background card
    dwg.add(
        dwg.rect(
            insert=(0.5, 0.5),
            size=(width - 1, height - 1),
            rx=RADIUS,
            ry=RADIUS,
            fill=COLORS["card"],
            stroke=COLORS["border"],
            stroke_width=1,
        )
    )

    dwg.add(
        dwg.text(
            "Contribution Calendar",
            insert=(24, 34),
            font_family=FONT_STACK,
            font_size="15px",
            font_weight="600",
            fill=COLORS["text"],
        )
    )
    dwg.add(
        dwg.text(
            "Daily contributions · last 12 months",
            insert=(24, 52),
            font_family=FONT_STACK,
            font_size="11.5px",
            fill=COLORS["subtext"],
        )
    )

    all_counts = [
        day["contributionCount"]
        for week in calendar_weeks
        for day in week["contributionDays"]
    ]
    max_count = max(all_counts) if all_counts else 0

    # Month labels with collision avoidance
    shown_months = set()
    last_x = -1000
    MIN_LABEL_DISTANCE = 38

    for w_idx, week in enumerate(calendar_weeks):
        days = week["contributionDays"]
        if not days:
            continue

        d = _dt.datetime.strptime(days[0]["date"], "%Y-%m-%d").date()

        if d.month in shown_months:
            continue

        x = left_pad + w_idx * (cell + gap)

        if x - last_x < MIN_LABEL_DISTANCE:
            continue

        shown_months.add(d.month)
        last_x = x

        dwg.add(
            dwg.text(
                month_short_name(d.month),
                insert=(x, top_pad - 10),
                font_family=FONT_STACK,
                font_size="10px",
                font_weight="500",
                fill=COLORS["subtext"],
            )
        )

    # weekday labels (Mon / Wed / Fri) down the left side
    for weekday_idx, label in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = top_pad + weekday_idx * (cell + gap) + cell - 1
        dwg.add(
            dwg.text(
                label,
                insert=(4, y),
                font_family=FONT_STACK,
                font_size="9.5px",
                fill=COLORS["subtext"],
            )
        )

    # the grid itself
    for w_idx, week in enumerate(calendar_weeks):
        for day in week["contributionDays"]:
            weekday = day["weekday"]  # 0 = Sunday ... 6 = Saturday
            count = day["contributionCount"]
            x = left_pad + w_idx * (cell + gap)
            y = top_pad + weekday * (cell + gap)
            color = _bucket_color(count, max_count)
            dwg.add(
                dwg.rect(
                    insert=(x, y),
                    size=(cell, cell),
                    rx=2.5,
                    ry=2.5,
                    fill=color,
                )
            )

    # legend: Less -> More
    legend_y = height - 22
    dwg.add(
        dwg.text(
            "Less",
            insert=(left_pad, legend_y + 8),
            font_family=FONT_STACK,
            font_size="9.5px",
            fill=COLORS["subtext"],
        )
    )
    swatch_x = left_pad + 32
    for i, color in enumerate(_INTENSITY_COLORS):
        dwg.add(
            dwg.rect(
                insert=(swatch_x + i * (cell + 3), legend_y),
                size=(cell, cell),
                rx=2.5,
                ry=2.5,
                fill=color,
            )
        )
    dwg.add(
        dwg.text(
            "More",
            insert=(swatch_x + len(_INTENSITY_COLORS) * (cell + 3) + 6, legend_y + 8),
            font_family=FONT_STACK,
            font_size="9.5px",
            fill=COLORS["subtext"],
        )
    )

    total = sum(all_counts)
    dwg.add(
        dwg.text(
            f"{total:,} contributions in the last year",
            insert=(width - 24, legend_y + 8),
            font_family=FONT_STACK,
            font_size="10.5px",
            fill=COLORS["subtext"],
            text_anchor="end",
        )
    )

    return dwg.tostring()
