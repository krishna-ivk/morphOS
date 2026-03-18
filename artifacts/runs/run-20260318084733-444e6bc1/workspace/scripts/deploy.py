from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    run_id = sys.argv[1] if len(sys.argv) > 1 else "local-run"
    out_dir = (
        Path(sys.argv[2]).resolve()
        if len(sys.argv) > 2
        else Path.cwd() / "artifacts" / "current"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "simulated",
        "message": "Deployment is simulated in the local MVP runtime.",
    }
    (out_dir / "deploy_receipt.json").write_text(json.dumps(payload, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
