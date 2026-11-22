
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class AgentMessage:
    sender: str
    recipient: str
    message_type: str
    task_id: str
    payload: dict[str, Any] = field(
        default_factory=dict
    )
    message_id: str = field(
        default_factory=lambda: str(uuid4())
    )
    timestamp: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )
