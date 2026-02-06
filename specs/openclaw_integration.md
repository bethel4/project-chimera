# OpenClaw Integration Specification

## Overview
OpenClaw is an "Agent Social Network" protocol that enables AI agents to discover, communicate, and collaborate with other autonomous agents. Project Chimera agents will integrate with OpenClaw to participate in the broader ecosystem of agent-to-agent interactions.

## Strategic Context

### What is OpenClaw?
OpenClaw represents the emergence of "Social Media for Bots" - a protocol layer where AI agents can:
- Publish their availability and capabilities
- Discover other agents by niche, topic, or capability
- Communicate and negotiate collaborations
- Form agent-to-agent partnerships

### Why Integrate?
1. **Network Effects**: Agents become more valuable when they can collaborate
2. **Discovery**: Other agents can find Chimera agents for partnerships
3. **Ecosystem Participation**: Positions Chimera as a first-class citizen in the agent economy
4. **Future-Proofing**: As agent-to-agent commerce grows, early integration provides competitive advantage

## Integration Architecture

### MCP Server: mcp-server-openclaw
We will create a dedicated MCP server that wraps OpenClaw protocol interactions, following the same pattern as other MCP servers (twitter, weaviate, coinbase).

**Transport**: SSE (Server-Sent Events) for remote OpenClaw API

### MCP Resources

#### Resource: `openclaw://agents/available`
**Description**: Lists all agents currently available for collaboration on the OpenClaw network.

**Response Schema**:
{
  "agents": [
    {
      "agent_id": "string",
      "name": "string",
      "niche": ["fashion", "tech", "lifestyle"],
      "status": "available | busy | offline",
      "capabilities": ["content_creation", "trend_analysis"],
      "engagement_metrics": {
        "followers": 10000,
        "avg_engagement_rate": 0.05
      }
    }
  ]
}

#### Resource: `openclaw://agents/me/status`
**Description**: Current status of this Chimera agent as seen by other agents on OpenClaw.

**Response Schema**:
{
  "agent_id": "string",
  "name": "string",
  "status": "available | busy | offline",
  "current_campaign": "string | null",
  "niche_tags": ["string"],
  "available_for_collaboration": true,
  "last_updated": "iso-timestamp"
}

#### Resource: `openclaw://messages/incoming`
**Description**: Incoming messages from other agents on the OpenClaw network.

**Response Schema**:
{
  "messages": [
    {
      "message_id": "uuid",
      "from_agent_id": "string",
      "from_agent_name": "string",
      "subject": "string",
      "body": "string",
      "message_type": "collaboration_request | partnership_proposal | info_query",
      "timestamp": "iso-timestamp",
      "read": false
    }
  ]
}

### MCP Tools

#### Tool: `openclaw.publish_status`
**Description**: Updates this agent's public status on the OpenClaw network.

**Input Schema**:
{
  "status": "available | busy | offline",
  "current_campaign": "string | null",
  "niche_tags": ["string"],
  "available_for_collaboration": boolean,
  "capabilities": ["string"]
}

#### Tool: `openclaw.send_message`
**Description**: Sends a message to another agent on the OpenClaw network.

**Input Schema**:
{
  "to_agent_id": "string",
  "subject": "string",
  "body": "string",
  "message_type": "collaboration_request | partnership_proposal | info_query"
}

#### Tool: `openclaw.discover_agents`
**Description**: Searches for agents matching criteria.

**Input Schema**:
{
  "niche": ["string"],
  "capabilities": ["string"],
  "min_followers": "integer | null",
  "status": "available | busy | offline | all"
}

## Privacy & Security
Only publish public status/capabilities. Never expose private memories, keys, wallets, or internal queues.

## Testing Strategy
- **Unit tests**: MCP handlers
- **Integration tests**: OpenClaw sandbox API
