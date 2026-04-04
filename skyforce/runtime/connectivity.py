"""Real connectivity detection - replaces stubbed always-true."""

from __future__ import annotations

import subprocess
import socket
from pathlib import Path


class ConnectivityManager:
    """Detects actual connectivity mode by probing network and deployment endpoints."""

    def __init__(self, probe_urls: list[str] | None = None):
        self.probe_urls = probe_urls or [
            "https://api.github.com",
            "https://registry.npmjs.org",
        ]

    def detect_mode(self) -> str:
        if self._is_deploy_enabled():
            return "deploy_enabled"
        if self._has_internet():
            return "online_read"
        return "offline"

    def _is_deploy_enabled(self) -> bool:
        return self._can_reach("https://api.github.com") and self._can_reach(
            "https://registry.npmjs.org"
        )

    def _has_internet(self) -> bool:
        return self._can_reach("https://www.google.com") or self._can_reach(
            "https://cloudflare.com"
        )

    def _can_reach(self, url: str, timeout: int = 3) -> bool:
        try:
            host = url.split("//")[1].split("/")[0]
            port = 443
            sock = socket.create_connection((host, port), timeout=timeout)
            sock.close()
            return True
        except (socket.timeout, socket.error, OSError, IndexError):
            return False

    def check_connectivity(self) -> dict[str, str]:
        mode = self.detect_mode()
        details = {
            "mode": mode,
            "deploy_enabled": mode == "deploy_enabled",
            "online_read": mode == "online_read",
            "offline": mode == "offline",
        }
        return details
