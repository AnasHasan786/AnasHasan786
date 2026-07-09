#!/usr/bin/env python3
"""
dashboard.py
-------------
Entry point run nightly by .github/workflows/dashboard.yml.

    python scripts/dashboard.py

Reads:
    GH_TOKEN          (required)  a PAT with `read:user` + `repo` scope
    GITHUB_USERNAME    (optional) defaults to AnasHasan786

Writes (always all six, or fails loudly — never partial/half-updated output):
    assets/dashboard/kpi_cards.svg
    assets/dashboard/weekly_activity.svg
    assets/dashboard/commit_trend.svg
    assets/dashboard/repo_growth.svg
    assets/dashboard/language_distribution.svg
    assets/dashboard/contribution_calendar.svg
"""

from __future__ import annotations

import os
import sys

from github_api import GitHubAPIError, build_dashboard_data
from charts import (
    generate_kpi_cards,
    generate_weekly_activity_chart,
    generate_commit_trend_chart,
    generate_repo_growth_chart,
    generate_language_distribution_chart,
)
from heatmap import generate_contribution_calendar
from utils import ASSETS_DIR, load_config


def _write(filename: str, content: str) -> None:
    path = os.path.join(ASSETS_DIR, filename)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"[dashboard] wrote {path} ({len(content):,} bytes)")


def main() -> int:
    config = load_config()
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    # Priority: GITHUB_USERNAME env var (set in the workflow) > config.yaml > default.
    username = os.environ.get("GITHUB_USERNAME") or config.get("username", "AnasHasan786")

    try:
        data = build_dashboard_data(token, username, config)
    except GitHubAPIError as exc:
        print(f"[dashboard] FATAL: {exc}", file=sys.stderr)
        return 1

    _write("kpi_cards.svg", generate_kpi_cards(data))
    _write("weekly_activity.svg", generate_weekly_activity_chart(data["weekly_activity"]))
    _write("commit_trend.svg", generate_commit_trend_chart(data["commit_trend"]))
    _write("repo_growth.svg", generate_repo_growth_chart(data["repo_growth"]))
    _write("language_distribution.svg", generate_language_distribution_chart(data["languages"]))
    _write("contribution_calendar.svg", generate_contribution_calendar(data["calendar_weeks"]))

    print("[dashboard] All 6 SVG assets generated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
