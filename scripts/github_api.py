"""
github_api.py
--------------
All network access to GitHub lives here. Two APIs are used, deliberately:

* GraphQL (`https://api.github.com/graphql`) — one round trip for profile
  totals, follower/following counts, pull-request/commit contribution
  totals, and the full contribution calendar (used for both the weekly
  activity chart and the custom heatmap).

* REST (`https://api.github.com`) — paginated repository listing (stars,
  primary language, creation date) which is far simpler to page through
  with REST than with GraphQL cursors, plus the Search API for a
  lifetime pull-request count that isn't limited to the last 12 months.

Every public method returns plain Python data structures (dicts/lists) —
no GitHub-shaped objects leak into charts.py / heatmap.py.
"""

from __future__ import annotations

import collections
import datetime as _dt
import sys
import time
from typing import Any

import requests

GRAPHQL_URL = "https://api.github.com/graphql"
REST_URL = "https://api.github.com"

REQUEST_TIMEOUT = 30
MAX_RETRIES = 3


class GitHubAPIError(RuntimeError):
    pass


class GitHubDataFetcher:
    def __init__(self, token: str, username: str):
        if not token:
            raise GitHubAPIError(
                "No GitHub token provided. Set the GH_PAT repository secret "
                "and expose it to the workflow as the GH_TOKEN env var."
            )
        self.token = token
        self.username = username
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": f"{username}-github-analytics-dashboard",
            }
        )

    # ------------------------------------------------------------------
    # low level request helpers with basic retry/backoff
    # ------------------------------------------------------------------
    def _post_graphql(self, query: str, variables: dict | None = None) -> dict:
        last_error = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.post(
                    GRAPHQL_URL,
                    json={"query": query, "variables": variables or {}},
                    timeout=REQUEST_TIMEOUT,
                )
                if resp.status_code == 401:
                    raise GitHubAPIError(
                        "GitHub rejected the token (401). Check that GH_PAT "
                        "is valid and has at least 'read:user' + 'repo' scope."
                    )
                resp.raise_for_status()
                payload = resp.json()
                if "errors" in payload and payload["errors"]:
                    raise GitHubAPIError(f"GraphQL errors: {payload['errors']}")
                return payload["data"]
            except (requests.RequestException, GitHubAPIError) as exc:
                last_error = exc
                if attempt < MAX_RETRIES:
                    time.sleep(2 * attempt)
                    continue
        raise GitHubAPIError(f"GraphQL request failed after retries: {last_error}")

    def _get_rest(self, path: str, params: dict | None = None) -> Any:
        last_error = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self.session.get(
                    f"{REST_URL}{path}", params=params, timeout=REQUEST_TIMEOUT
                )
                resp.raise_for_status()
                return resp.json()
            except requests.RequestException as exc:
                last_error = exc
                if attempt < MAX_RETRIES:
                    time.sleep(2 * attempt)
                    continue
        raise GitHubAPIError(f"REST request failed for {path}: {last_error}")

    # ------------------------------------------------------------------
    # GraphQL: profile + contribution calendar
    # ------------------------------------------------------------------
    _PROFILE_QUERY = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        name
        login
        followers { totalCount }
        following { totalCount }
        repositories(
            privacy: PUBLIC
            isFork: false
            first: 100
        ) {
            totalCount
        }
        contributionsCollection(from: $from, to: $to) {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          totalPullRequestReviewContributions
          commitContributionsByRepository(maxRepositories: 100) {
            repository { nameWithOwner }
          }
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                weekday
                contributionCount
              }
            }
          }
        }
      }
    }
    """

    def get_profile_and_calendar(self) -> dict:
        now = _dt.datetime.utcnow().replace(microsecond=0)
        one_year_ago = now - _dt.timedelta(days=365)
        data = self._post_graphql(
            self._PROFILE_QUERY,
            {
                "login": self.username,
                "from": one_year_ago.isoformat() + "Z",
                "to": now.isoformat() + "Z",
            },
        )
        user = data.get("user")
        if not user:
            raise GitHubAPIError(f"GitHub user '{self.username}' was not found.")

        cc = user["contributionsCollection"]
        return {
            "name": user.get("name") or user["login"],
            "login": user["login"],
            "followers": user["followers"]["totalCount"],
            "following": user["following"]["totalCount"],
            "public_repos": user["repositories"]["totalCount"],
            "total_commit_contributions": cc["totalCommitContributions"],
            "total_pr_contributions": cc["totalPullRequestContributions"],
            "total_issue_contributions": cc["totalIssueContributions"],
            "total_review_contributions": cc["totalPullRequestReviewContributions"],
            "contributed_repos": len(cc["commitContributionsByRepository"]),
            "calendar_weeks": cc["contributionCalendar"]["weeks"],
            "total_contributions": cc["contributionCalendar"]["totalContributions"],
        }

    # ------------------------------------------------------------------
    # REST: full list of owned, non-fork public repositories
    # ------------------------------------------------------------------
    def get_repositories(self) -> list[dict]:
        repos: list[dict] = []
        page = 1
        while True:
            batch = self._get_rest(
                f"/users/{self.username}/repos",
                params={
                    "type": "owner",
                    "per_page": 100,
                    "page": page,
                    "sort": "created",
                    "direction": "asc",
                },
            )
            if not batch:
                break
            for repo in batch:
                if repo.get("fork") or repo.get("private"):
                    continue
                repos.append(
                    {
                        "name": repo["name"],
                        "stargazers_count": repo.get("stargazers_count", 0),
                        "language": repo.get("language"),
                        "created_at": repo["created_at"],
                    }
                )
            if len(batch) < 100:
                break
            page += 1
        return repos

    # ------------------------------------------------------------------
    # REST Search API: lifetime pull request count (not limited to 1yr)
    # ------------------------------------------------------------------
    def get_lifetime_pull_request_count(self) -> int:
        result = self._get_rest(
            "/search/issues", params={"q": f"author:{self.username} type:pr"}
        )
        return int(result.get("total_count", 0))

    # ------------------------------------------------------------------
    # Derived, chart-ready aggregates
    # ------------------------------------------------------------------
    @staticmethod
    def total_stars(repos: list[dict]) -> int:
        return sum(r["stargazers_count"] for r in repos)

    @staticmethod
    def language_distribution(repos: list[dict], top_n: int = 6) -> list[dict]:
        counts: collections.Counter = collections.Counter(
            r["language"] for r in repos if r.get("language")
        )
        total = sum(counts.values()) or 1
        ranked = counts.most_common()
        top = ranked[:top_n]
        rest = ranked[top_n:]
        result = [
            {"language": name, "count": count, "pct": round(count / total * 100, 1)}
            for name, count in top
        ]
        if rest:
            other_count = sum(c for _, c in rest)
            result.append(
                {
                    "language": "Other",
                    "count": other_count,
                    "pct": round(other_count / total * 100, 1),
                }
            )
        return result

    @staticmethod
    def repo_growth_by_month(repos: list[dict], months: int = 12) -> list[dict]:
        """Cumulative repository count for each of the last `months` months."""
        now = _dt.datetime.utcnow().date().replace(day=1)
        buckets = []
        for i in range(months - 1, -1, -1):
            year = now.year
            month = now.month - i
            while month <= 0:
                month += 12
                year -= 1
            buckets.append((year, month))

        created_dates = [
            _dt.datetime.strptime(r["created_at"][:10], "%Y-%m-%d").date()
            for r in repos
        ]

        result = []
        for year, month in buckets:
            bucket_end = _dt.date(year, month, 1)
            if month == 12:
                bucket_end = _dt.date(year + 1, 1, 1)
            else:
                bucket_end = _dt.date(year, month + 1, 1)
            cumulative = sum(1 for d in created_dates if d < bucket_end)
            result.append({"year": year, "month": month, "count": cumulative})
        return result

    @staticmethod
    def weekly_commit_activity(
        calendar_weeks: list[dict], num_weeks: int = 12
    ) -> list[dict]:
        """Sum contributionCount per ISO week for the last `num_weeks` weeks."""
        weeks = (
            calendar_weeks[-num_weeks:]
            if len(calendar_weeks) > num_weeks
            else calendar_weeks
        )
        result = []
        for week in weeks:
            days = week["contributionDays"]
            total = sum(d["contributionCount"] for d in days)
            start_date = days[0]["date"] if days else None
            result.append({"week_start": start_date, "commits": total})
        return result

    @staticmethod
    def commit_trend_cumulative(
        calendar_weeks: list[dict], num_weeks: int = 12
    ) -> list[dict]:
        weekly = GitHubDataFetcher.weekly_commit_activity(calendar_weeks, num_weeks)
        running = 0
        result = []
        for w in weekly:
            running += w["commits"]
            result.append({"week_start": w["week_start"], "cumulative": running})
        return result


def build_dashboard_data(token: str, username: str, config: dict | None = None) -> dict:
    """Single entry point used by dashboard.py — fetches + shapes everything.

    `config` accepts the dict produced by utils.load_config() (weeks/months/
    top_n knobs from config.yaml); sensible defaults are used if omitted.
    """
    config = config or {}
    weeks = int(config.get("weekly_activity_weeks", 12))
    months = int(config.get("repo_growth_months", 12))
    top_n = int(config.get("language_top_n", 6))

    fetcher = GitHubDataFetcher(token, username)

    print(
        f"[github_api] Fetching profile + contribution calendar for {username}...",
        file=sys.stderr,
    )
    profile = fetcher.get_profile_and_calendar()

    print("[github_api] Fetching repository list...", file=sys.stderr)
    repos = fetcher.get_repositories()

    print("[github_api] Fetching lifetime pull request count...", file=sys.stderr)
    try:
        lifetime_prs = fetcher.get_lifetime_pull_request_count()
    except GitHubAPIError:
        # Search API can rate-limit independently of GraphQL; fall back
        # gracefully to the last-12-months figure rather than failing the run.
        lifetime_prs = profile["total_pr_contributions"]

    stars = fetcher.total_stars(repos)
    languages = fetcher.language_distribution(repos, top_n=top_n)
    repo_growth = fetcher.repo_growth_by_month(repos, months=months)
    weekly_activity = fetcher.weekly_commit_activity(
        profile["calendar_weeks"], num_weeks=weeks
    )
    commit_trend = fetcher.commit_trend_cumulative(
        profile["calendar_weeks"], num_weeks=weeks
    )

    return {
        "profile": profile,
        "repos": repos,
        "stars": stars,
        "pull_requests": lifetime_prs,
        "languages": languages,
        "repo_growth": repo_growth,
        "weekly_activity": weekly_activity,
        "commit_trend": commit_trend,
        "calendar_weeks": profile["calendar_weeks"],
        "generated_at": _dt.datetime.utcnow().isoformat() + "Z",
    }
