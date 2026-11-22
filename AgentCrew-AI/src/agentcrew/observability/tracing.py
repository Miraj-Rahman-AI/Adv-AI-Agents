
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class TraceRecorder:
    def __init__(self):
        self.events: list[dict[str, Any]] = []

    def record(
        self,
        event: str,
        **details: Any,
    ) -> None:
        self.events.append(
            {
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
                "event": event,
                **details,
            }
        )

    def export_jsonl(self, path: Path) -> None:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as handle:
            for event in self.events:
                handle.write(
                    json.dumps(
                        event,
                        ensure_ascii=False,
                    )
                    + "\n"
                )
