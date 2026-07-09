"""
utils.py
---------
Shared constants and helper functions used across the dashboard generator:
color palette, typography, small SVG building blocks, number/date formatting,
and the Jinja2 environment used to render the outer "card" wrapper that every
chart sits inside of.

Keeping this logic in one place is what makes every chart in the dashboard
look consistent (same border radius, same border color, same title style).
"""

from __future__ import annotations

import datetime as _dt
import os
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPTS_DIR)
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets", "dashboard")
CONFIG_PATH = os.path.join(ROOT_DIR, "config.yaml")

os.makedirs(ASSETS_DIR, exist_ok=True)

_DEFAULT_CONFIG = {
    "username": "AnasHasan786",
    "weekly_activity_weeks": 12,
    "repo_growth_months": 12,
    "language_top_n": 6,
}


def load_config() -> dict:
    """Load config.yaml (PyYAML), falling back to sane defaults if it's
    missing or malformed so a bad edit never breaks the nightly workflow."""
    cfg = dict(_DEFAULT_CONFIG)
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
            loaded = yaml.safe_load(fh) or {}
        if isinstance(loaded, dict):
            cfg.update({k: v for k, v in loaded.items() if v is not None})
    except FileNotFoundError:
        pass
    return cfg

# ----------------------------------------------------------------------------
# Color palette (matches the profile README exactly — no red/orange/yellow,
# no rainbow accents, everything derived from the blue family).
# ----------------------------------------------------------------------------
COLORS = {
    "bg": "#0D1117",
    "card": "#161B22",
    "card_alt": "#1B222C",
    "primary": "#00BFFF",
    "secondary": "#38BDF8",
    "border": "#30363D",
    "text": "#FFFFFF",
    "subtext": "#8B949E",
    "grid": "#21262D",
}

# A restrained ramp of blues used anywhere multiple series/slices are needed
# (donut chart, legend swatches). Deliberately monochrome-blue, per brief.
BLUE_SHADES = [
    "#00BFFF",
    "#38BDF8",
    "#0EA5E9",
    "#0284C7",
    "#0369A1",
    "#075985",
    "#0C4A6E",
]

FONT_STACK = (
    "'Segoe UI', ui-sans-serif, system-ui, -apple-system, "
    "'Helvetica Neue', Arial, sans-serif"
)
FONT_MONO_STACK = (
    "'SF Mono', 'JetBrains Mono', ui-monospace, 'Cascadia Code', "
    "Consolas, monospace"
)

RADIUS = 12  # standard corner radius used on every card (8-12px per brief)

# ----------------------------------------------------------------------------
# Jinja2 environment
# ----------------------------------------------------------------------------
_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(disabled_extensions=("j2",), default=False),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_card(
    title: str,
    subtitle: str,
    width: int,
    height: int,
    inner_svg: str,
    icon_svg: str = "",
) -> str:
    """Render a chart/KPI block inside the shared card wrapper template."""
    template = _env.get_template("card_wrapper.svg.j2")
    return template.render(
        colors=COLORS,
        font=FONT_STACK,
        radius=RADIUS,
        title=title,
        subtitle=subtitle,
        width=width,
        height=height,
        inner_svg=inner_svg,
        icon_svg=icon_svg,
    )


# ----------------------------------------------------------------------------
# Small SVG building blocks
# ----------------------------------------------------------------------------
def linear_gradient(gid: str, x1, y1, x2, y2, stops) -> str:
    """
    stops: list of (offset_percent, color, opacity) tuples.
    """
    stop_tags = "\n".join(
        f'      <stop offset="{off}%" stop-color="{color}" stop-opacity="{op}" />'
        for off, color, op in stops
    )
    return (
        f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">\n'
        f"{stop_tags}\n"
        f"    </linearGradient>"
    )


def rounded_rect(x, y, w, h, rx, fill, stroke=None, stroke_width=1, opacity=1) -> str:
    stroke_attr = f'stroke="{stroke}" stroke-width="{stroke_width}"' if stroke else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" ry="{rx}" '
        f'fill="{fill}" {stroke_attr} opacity="{opacity}" />'
    )


def text(x, y, content, size=13, color=COLORS["text"], weight=500, anchor="start",
          family=FONT_STACK, letter_spacing=None, opacity=1) -> str:
    ls = f'letter-spacing="{letter_spacing}"' if letter_spacing else ""
    safe = (
        str(content)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}" '
        f'{ls} opacity="{opacity}">{safe}</text>'
    )


def smooth_path(points):
    """
    Build a smooth cubic-bezier SVG path ('d' attribute) through a list of
    (x, y) points using a simple Catmull-Rom -> Bezier conversion. Produces
    the gentle, modern curve used in the line/area charts.
    """
    if len(points) < 2:
        return ""
    d = f"M {points[0][0]:.2f} {points[0][1]:.2f} "
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2

        c1x = p1[0] + (p2[0] - p0[0]) / 6
        c1y = p1[1] + (p2[1] - p0[1]) / 6
        c2x = p2[0] - (p3[0] - p1[0]) / 6
        c2y = p2[1] - (p3[1] - p1[1]) / 6

        d += f"C {c1x:.2f} {c1y:.2f} {c2x:.2f} {c2y:.2f} {p2[0]:.2f} {p2[1]:.2f} "
    return d.strip()


# ----------------------------------------------------------------------------
# Formatting helpers
# ----------------------------------------------------------------------------
def format_number(n) -> str:
    """1234 -> '1.2k', 1200000 -> '1.2M', else plain int string."""
    try:
        n = float(n)
    except (TypeError, ValueError):
        return str(n)
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M".replace(".0M", "M")
    if n >= 1_000:
        return f"{n / 1_000:.1f}k".replace(".0k", "k")
    return str(int(n))


def month_short_name(month: int) -> str:
    return [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    ][month - 1]


def weekday_short_name(idx: int) -> str:
    """idx: 0=Sunday ... 6=Saturday (matches GitHub's contribution weekday index)."""
    return ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][idx]


def iso_monday(date: _dt.date) -> _dt.date:
    """Return the Monday of the ISO week containing `date`."""
    return date - _dt.timedelta(days=date.weekday())


def utc_today() -> _dt.date:
    return _dt.datetime.utcnow().date()
