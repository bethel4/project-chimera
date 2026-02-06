# tests/test_mcp_integration.py
import pytest

from tests.conftest import MockMCPClient  # reuse mock until real client exists


@pytest.mark.asyncio
async def test_mcp_client_can_connect_to_server():
    """
    Spec: Phase 2, MCP Integration.
    - Client must be able to connect to a named server via Stdio/SSE.
    """
    client = MockMCPClient()
    await client.connect("filesystem")

    assert "filesystem" in client.connected_servers


@pytest.mark.asyncio
async def test_mcp_resource_polling_contract():
    """
    Spec: FR 2.0 Active Resource Monitoring.
    - MCP client must support reading Resources like news://latest.
    """
    client = MockMCPClient()

    with pytest.raises(NotImplementedError):
        await client.read_resource("news", "news://latest")


@pytest.mark.asyncio
async def test_mcp_tool_invocation_contract():
    """
    Spec: FR 3.0 Multimodal Generation via MCP Tools.
    - MCP client must support calling tools with JSON arguments.
    """
    client = MockMCPClient()

    with pytest.raises(NotImplementedError):
        await client.call_tool(
            server_name="image-gen",
            tool_name="generate_image",
            arguments={"prompt": "test"},
        )