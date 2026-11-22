
from __future__ import annotations

from typing import Any

from agentcrew.communication.message import AgentMessage


class MessageBus:
    def __init__(self):
        self._messages: list[AgentMessage] = []

    def publish(
        self,
        sender: str,
        recipient: str,
        message_type: str,
        task_id: str,
        payload: dict[str, Any] | None = None,
    ) -> AgentMessage:
        message = AgentMessage(
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            task_id=task_id,
            payload=payload or {},
        )

        self._messages.append(message)
        return message

    def get_messages(
        self,
        recipient: str | None = None,
        task_id: str | None = None,
    ) -> list[AgentMessage]:
        result = self._messages

        if recipient is not None:
            result = [
                message
                for message in result
                if message.recipient == recipient
            ]

        if task_id is not None:
            result = [
                message
                for message in result
                if message.task_id == task_id
            ]

        return list(result)

    def count(self) -> int:
        return len(self._messages)
