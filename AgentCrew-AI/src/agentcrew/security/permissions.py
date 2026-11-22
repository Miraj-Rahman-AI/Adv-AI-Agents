
from dataclasses import dataclass, field


@dataclass(frozen=True)
class AuthorizationContext:
    """Trusted application-level authorization limits."""

    allowed_tools: frozenset[str] = field(
        default_factory=frozenset
    )
    allowed_actions: frozenset[str] = field(
        default_factory=frozenset
    )
    allowed_resources: frozenset[str] = field(
        default_factory=frozenset
    )
