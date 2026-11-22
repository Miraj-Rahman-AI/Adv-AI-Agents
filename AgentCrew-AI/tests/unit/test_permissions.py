
import pytest

from agentcrew.security import (
    AuthorizationContext,
    PolicyEngine,
)


@pytest.fixture
def policy():
    return PolicyEngine(
        agent_rules={
            "researcher": {
                "tools": ["document_search"]
            },
            "analyst": {
                "tools": []
            },
        },
        tool_rules={
            "document_search": {
                "action": "read",
                "resource": "documents",
                "allowed_roles": ["researcher"],
            }
        },
    )


@pytest.fixture
def authorization():
    return AuthorizationContext(
        allowed_tools=frozenset({
            "document_search"
        }),
        allowed_actions=frozenset({"read"}),
        allowed_resources=frozenset({
            "documents"
        }),
    )


def test_authorized_research_tool(
    policy,
    authorization,
):
    policy.authorize(
        role="researcher",
        tool_name="document_search",
        action="read",
        resource="documents",
        authorization=authorization,
    )


def test_unauthorized_agent_role(
    policy,
    authorization,
):
    with pytest.raises(PermissionError):
        policy.authorize(
            role="analyst",
            tool_name="document_search",
            action="read",
            resource="documents",
            authorization=authorization,
        )


def test_unauthorized_resource(
    policy,
    authorization,
):
    with pytest.raises(PermissionError):
        policy.authorize(
            role="researcher",
            tool_name="document_search",
            action="read",
            resource="private_records",
            authorization=authorization,
        )


def test_missing_user_authorization(
    policy,
):
    empty = AuthorizationContext()

    with pytest.raises(PermissionError):
        policy.authorize(
            role="researcher",
            tool_name="document_search",
            action="read",
            resource="documents",
            authorization=empty,
        )
