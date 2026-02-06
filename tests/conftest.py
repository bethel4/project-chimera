# tests/conftest.py
import pytest
from typing import Dict, Any

class MockMCPClient:
    """Very simple mock MCP client used only for tests at this stage."""

    def __init__(self):
        self.connected_servers = set()

    async def connect(self, server_name: str) -> None:
        # In real code: open stdio/SSE connection
        self.connected_servers.add(server_name)

    async def read_resource(self, server_name: str, resource: str) -> Dict[str, Any]:
        # In real code: JSON-RPC call
        raise NotImplementedError("MockMCPClient.read_resource not implemented")

    async def call_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        # In real code: JSON-RPC call
        raise NotImplementedError("MockMCPClient.call_tool not implemented")


class MockRedis:
    """Simple in-memory Redis-like store for tests."""
    def __init__(self):
        self.store: Dict[str, Any] = {}

    async def get(self, key: str):
        return self.store.get(key)

    async def set(self, key: str, value: Any):
        self.store[key] = value

    async def flushall(self):
        self.store.clear()


@pytest.fixture
def mock_mcp_client():
    return MockMCPClient()


@pytest.fixture
def mock_redis():
    return MockRedis()


@pytest.fixture
def sample_persona():
    """
    Minimal sample persona that would normally come from SOUL.md + Weaviate.
    """
    return {
        "id": "agent-demo-1",
        "name": "Chimera Demo Agent",
        "voice_traits": ["witty", "insightful"],
        "directives": ["never give medical advice", "be transparent about being AI"],
    }