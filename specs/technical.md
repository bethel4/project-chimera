cat > specs/technical.md << 'EOF'
# Technical Specifications

## API Contracts

### Task Schema (JSON)
{
  "task_id": "uuid-v4-string",
  "task_type": "generate_content | reply_comment | execute_transaction | fetch_trends",
  "priority": "high | medium | low",
  "context": {
    "goal_description": "string",
    "persona_constraints": ["string"],
    "required_resources": ["mcp://twitter/mentions/123", "mcp://memory/recent"],
    "budget_limit": "float (USDC)"
  },
  "assigned_worker_id": "string | null",
  "created_at": "iso-timestamp",
  "status": "pending | in_progress | review | complete | rejected"
}
## Result Schema (JSON)
{
  "result_id": "uuid-v4-string",
  "task_id": "uuid-v4-string",
  "worker_id": "string",
  "output": {
    "type": "text | image | video | transaction",
    "content": "string | url",
    "metadata": {}
  },
  "confidence_score": "float (0.0-1.0)",
  "reasoning_trace": "string",
  "created_at": "iso-timestamp"
}
## GlobalState Schema (JSON)
{
  "state_version": "integer",
  "campaign_id": "uuid-v4-string",
  "active_goals": [
    {
      "goal_id": "uuid-v4-string",
      "description": "string",
      "priority": "high | medium | low",
      "status": "active | paused | completed"
    }
  ],
  "budget": {
    "total_usdc": "float",
    "spent_today_usdc": "float",
    "daily_limit_usdc": "float"
  },
  "trends": [
    {
      "topic": "string",
      "relevance_score": "float (0.0-1.0)",
      "detected_at": "iso-timestamp"
    }
  ],
  "last_updated": "iso-timestamp"
}
## MCP Tool Definition: post_content
{
  "name": "post_content",
  "description": "Publishes text and media to a connected social platform.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "platform": {
        "type": "string",
        "enum": ["twitter", "instagram", "threads", "tiktok"]
      },
      "text_content": {
        "type": "string",
        "description": "The body of the post/tweet."
      },
      "media_urls": {
        "type": "array",
        "items": {"type": "string", "format": "uri"}
      },
      "disclosure_level": {
        "type": "string",
        "enum": ["automated", "assisted", "none"]
      }
    },
    "required": ["platform", "text_content"]
  }
}
## MCP Tool Definition: generate_image  
{
  "name": "generate_image",
  "description": "Generates an image using AI with character consistency.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "prompt": {
        "type": "string",
        "description": "Image generation prompt"
      },
      "character_reference_id": {
        "type": "string",
        "description": "LoRA or style ID for character consistency"
      },
      "style": {
        "type": "string",
        "enum": ["photorealistic", "illustration", "3d-render"]
      }
    },
    "required": ["prompt", "character_reference_id"]
  }
}
## MCP Tool Definition: execute_transaction
{
  "name": "execute_transaction",
  "description": "Executes an on-chain transaction via Coinbase AgentKit.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "action": {
        "type": "string",
        "enum": ["native_transfer", "erc20_transfer", "deploy_token"]
      },
      "to_address": {
        "type": "string",
        "pattern": "^0x[a-fA-F0-9]{40}$"
      },
      "amount_usdc": {
        "type": "number",
        "minimum": 0.01
      },
      "token_address": {
        "type": "string",
        "description": "Required for erc20_transfer"
      }
    },
    "required": ["action", "to_address", "amount_usdc"]
  }
}
## MCP Resource Definition: twitter_mentions
{
  "uri": "mcp://twitter/mentions/recent",
  "name": "Recent Mentions",
  "description": "Returns recent mentions of the agent on Twitter/X",
  "mimeType": "application/json"
}
## MCP Resource Definition: news_trends
{
  "uri": "mcp://news/ethiopia/fashion/trends",
  "name": "Fashion Trends Ethiopia",
  "description": "Aggregated RSS feeds for fashion trends in Ethiopia",
  "mimeType": "application/json"
}
## MCP Resource Definition: agent_memory
{
  "uri": "mcp://news/ethiopia/fashion/trends",
  "name": "Fashion Trends Ethiopia",
  "description": "Aggregated RSS feeds for fashion trends in Ethiopia",
  "mimeType": "application/json"
}
{
  "uri": "mcp://weaviate/memory/{agent_id}/semantic",
  "name": "Semantic Memory",
  "description": "Retrieves semantically relevant memories for the agent",
  "mimeType": "application/json"
}
### Database Schema (PostgreSQL)
## Agents Table

CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    soul_md_path TEXT NOT NULL,
    wallet_address VARCHAR(42) UNIQUE,
    status VARCHAR(20) DEFAULT 'sleeping', -- planning, working, judging, sleeping
    current_campaign_id UUID REFERENCES campaigns(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_agents_campaign ON agents(current_campaign_id);

## Campaigns Table
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    operator_id UUID REFERENCES users(id),
    goal_description TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'draft', -- draft, active, paused, completed
    budget_limit_usdc DECIMAL(18, 6),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaigns_operator ON campaigns(operator_id);
## Tasks Table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id),
    task_type VARCHAR(50) NOT NULL,
    priority VARCHAR(10) NOT NULL,
    context JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    assigned_worker_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_agent ON tasks(agent_id);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_context ON tasks USING GIN(context);
## Results Table
CREATE TABLE results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    worker_id VARCHAR(100) NOT NULL,
    output JSONB NOT NULL,
    confidence_score DECIMAL(3, 2) CHECK (confidence_score >= 0 AND confidence_score <= 1),
    reasoning_trace TEXT,
    judge_decision VARCHAR(20), -- approved, rejected, escalated
    hitl_reviewed BOOLEAN DEFAULT FALSE,
    hitl_reviewer_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_results_task ON results(task_id);
CREATE INDEX idx_results_confidence ON results(confidence_score);
CREATE INDEX idx_results_decision ON results(judge_decision);
CREATE INDEX idx_results_hitl ON results(hitl_reviewed) WHERE hitl_reviewed = FALSE;
## Users Table (Network Operators & Reviewers)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL, -- operator, reviewer, admin
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
## Transactions Table (On-Chain Ledger)
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id),
    tx_hash VARCHAR(66) UNIQUE NOT NULL,
    action VARCHAR(50) NOT NULL, -- native_transfer, erc20_transfer, deploy_token
    from_address VARCHAR(42) NOT NULL,
    to_address VARCHAR(42) NOT NULL,
    amount_usdc DECIMAL(18, 6) NOT NULL,
    network VARCHAR(20) DEFAULT 'base',
    status VARCHAR(20) DEFAULT 'pending', -- pending, confirmed, failed
    created_at TIMESTAMP DEFAULT NOW(),
    confirmed_at TIMESTAMP
);

CREATE INDEX idx_transactions_agent ON transactions(agent_id);
CREATE INDEX idx_transactions_hash ON transactions(tx_hash);
CREATE INDEX idx_transactions_status ON transactions(status);
## Agent Memories (Weaviate Schema)
{
  "class": "AgentMemory",
  "description": "Stores agent memories for RAG retrieval",
  "vectorizer": "text2vec-openai",
  "properties": [
    {
      "name": "agentId",
      "dataType": ["string"],
      "indexInverted": true
    },
    {
      "name": "content",
      "dataType": ["text"],
      "indexInverted": true
    },
    {
      "name": "timestamp",
      "dataType": ["date"]
    },
    {
      "name": "memoryType",
      "dataType": ["string"],
      "indexInverted": true
    },
    {
      "name": "engagementScore",
      "dataType": ["number"],
      "description": "For episodic memories: engagement metrics"
    },
    {
      "name": "tags",
      "dataType": ["string[]"],
      "description": "Semantic tags for filtering"
    }
  ]
}
## Redis Schema
## Task Queue
Key: task_queue:{agent_id}
Type: List
Value: JSON stringified Task object

## Review Queue
Key: review_queue:{agent_id}
Type: List
Value: JSON stringified Result object

## Global State
Key: global_state:{campaign_id}
Type: Hash
Fields: state_version, campaign_id, goals, budget, trends, last_updated
TTL: None (persistent)

## Episodic Cache (Short-term memory)
Key: episodic:{agent_id}:{timestamp}
Type: String (JSON)
TTL: 3600 seconds (1 hour)

## Daily Budget Tracking
Key: budget:{agent_id}:{date}
Type: String (float)
TTL: 86400 seconds (24 hours)

## MCP Server Requirements
## Required MCP Servers
1 mcp-server-weaviate
 . Tools: search_memory, store_memory, update_memory
 . Resources: mcp://weaviate/memory/{agent_id}/semantic
2.mcp-server-twitter
  .Tools: post_tweet, reply_tweet, like_tweet, get_mentions
  .Resources: mcp://twitter/mentions/recent, mcp://twitter/user/{id}/profile
3 mcp-server-coinbase
  .Tools: get_balance, execute_transaction, deploy_token
  .Resources: mcp://coinbase/wallet/{address}/balance
4 mcp-server-news
  .Tools: fetch_trends, search_articles
  .Resources: mcp://news/{region}/{category}/trends
5 mcp-server-image-gen
  .Tools: generate_image, upscale_image
  .Resources: None (stateless)
6 mcp-server-video-gen
  .Tools: generate_video, image_to_video
  .Resources: None (stateless)

## MCP Transport Configuration
  .Local Development: Stdio transport
  .Production: SSE (Server-Sent Events) transport
  .Connection Pool: Max 10 concurrent connections per MCP server

## API Endpoints (REST)
## Orchestrator API
## POST /api/campaigns

{
  "goal_description": "string",
  "budget_limit_usdc": 1000.00,
  "agent_ids": ["uuid-1", "uuid-2"]
}

GET /api/campaigns/{id}/status
Get campaign status and agent health

POST /api/agents/{id}/tasks
Manually inject a task (for testing)

## HITL Review API
GET /api/review/queue
Get pending items for human review
{
  "items": [
    {
      "result_id": "uuid",
      "task_type": "generate_content",
      "output": {...},
      "confidence_score": 0.75,
      "reasoning_trace": "string"
    }
  ]
}

POST /api/review/{result_id}/approve
Approve a result

POST /api/review/{result_id}/reject
Reject a result

POST /api/review/{result_id}/edit
Edit and approve a result

## Performance Requirements
  .Task processing latency: < 10 seconds (high priority)
  .Swarm horizontal scalability: 1,000+ concurrent agents
  .Database query latency: < 100ms (p95)
  .MCP tool call timeout: 30 seconds
  .Redis cache hit rate: > 80%
## Security Requirements
  .Wallet private keys: Stored in AWS Secrets Manager / HashiCorp Vault
  .API authentication: JWT tokens
  .MCP server authentication: API keys per server
  .Rate limiting: 100 requests/15min per IP
  .CSRF protection: Double-submit cookie pattern
EOF 