"""PR creation fallback using GitHub API when gh CLI is unavailable."""

from __future__ import annotations

import json
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any


class PRClient:
    """Creates pull requests via gh CLI or GitHub REST API fallback."""

    def __init__(self, repo_path: Path, token: str | None = None):
        self.repo_path = Path(repo_path)
        self.token = token or self._get_github_token()

    def create_pr(
        self,
        branch: str,
        base: str,
        title: str,
        body: str,
    ) -> str | None:
        """Create a PR, trying gh CLI first, then falling back to REST API."""
        result = self._try_gh_cli(branch, base, title, body)
        if result:
            return result
        return self._try_github_api(branch, base, title, body)

    def _try_gh_cli(self, branch: str, base: str, title: str, body: str) -> str | None:
        try:
            result = subprocess.run(
                [
                    "gh",
                    "pr",
                    "create",
                    "--base",
                    base,
                    "--head",
                    branch,
                    "--title",
                    title,
                    "--body",
                    body,
                ],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )
            return result.stdout.strip()
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
        ):
            return None

    def _try_github_api(
        self, branch: str, base: str, title: str, body: str
    ) -> str | None:
        if not self.token:
            return None

        repo = self._get_repo_slug()
        if not repo:
            return None

        url = f"https://api.github.com/repos/{repo}/pulls"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        }
        data = json.dumps(
            {
                "title": title,
                "body": body,
                "head": branch,
                "base": base,
            }
        ).encode("utf-8")

        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result.get("html_url")
        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            json.JSONDecodeError,
            OSError,
        ):
            return None

    def _get_repo_slug(self) -> str | None:
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
                timeout=10,
            )
            remote_url = result.stdout.strip()
            if "github.com" in remote_url:
                parts = remote_url.rstrip(".git").split("github.com/")[-1].split("/")
                if len(parts) == 2:
                    return f"{parts[0]}/{parts[1]}"
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, IndexError):
            pass
        return None

    def _get_github_token(self) -> str | None:
        try:
            result = subprocess.run(
                ["gh", "auth", "token"],
                capture_output=True,
                text=True,
                check=True,
                timeout=10,
            )
            return result.stdout.strip()
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
        ):
            import os

            return os.environ.get("GITHUB_TOKEN")

    def merge_pr(self, pr_url: str, method: str = "squash") -> bool:
        """Merge a PR by URL."""
        try:
            subprocess.run(
                ["gh", "pr", "merge", pr_url, f"--{method}", "--admin"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
                timeout=60,
            )
            return True
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
        ):
            return False

    def check_pr_status(self, pr_url: str) -> dict[str, Any]:
        """Check if a PR is mergeable."""
        try:
            result = subprocess.run(
                [
                    "gh",
                    "pr",
                    "view",
                    pr_url,
                    "--json",
                    "state,mergeable,mergeStateStatus",
                ],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )
            return json.loads(result.stdout)
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
            json.JSONDecodeError,
        ):
            return {"state": "unknown", "mergeable": "unknown"}
