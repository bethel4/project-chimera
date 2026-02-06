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
      "prompt": {"type": "string", "description": "Image generation prompt"},
      "character_reference_id": {"type": "string", "description": "LoRA or style ID for character consistency"},
      "style": {"type": "string", "enum": ["photorealistic", "illustration", "3d-render"]}
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
      "action": {"type": "string", "enum": ["native_transfer", "erc20_transfer", "deploy_token"]},
      "to_address": {"type": "string", "pattern": "^0x[a-fA-F0-9]{40}$"},
      "amount_usdc": {"type": "number", "minimum": 0.01},
      "token_address": {"type": "string", "description": "Required for erc20_transfer"}
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
    status VARCHAR(20) DEFAULT 'sleeping',
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
    status VARCHAR(20) DEFAULT 'draft',
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
    judge_decision VARCHAR(20),
    hitl_reviewed BOOLEAN DEFAULT FALSE,
    hitl_reviewer_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_results_task ON results(task_id);
CREATE INDEX idx_results_confidence ON results(confidence_score);
CREATE INDEX idx_results_decision ON results(judge_decision);
CREATE INDEX idx_results_hitl ON results(hitl_reviewed) WHERE hitl_reviewed = FALSE;

## Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

## Transactions Table
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id),
    tx_hash VARCHAR(66) UNIQUE NOT NULL,
    action VARCHAR(50) NOT NULL,
    from_address VARCHAR(42) NOT NULL,
    to_address VARCHAR(42) NOT NULL,
    amount_usdc DECIMAL(18, 6) NOT NULL,
    network VARCHAR(20) DEFAULT 'base',
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    confirmed_at TIMESTAMP
);

CREATE INDEX idx_transactions_agent ON transactions(agent_id);
CREATE INDEX idx_transactions_hash ON transactions(tx_hash);
CREATE INDEX idx_transactions_status ON transactions(status);

## MCP Server Requirements
1. mcp-server-weaviate
   - Tools: search_memory, store_memory, update_memory
   - Resources: mcp://weaviate/memory/{agent_id}/semantic
2. mcp-server-twitter
   - Tools: post_tweet, reply_tweet, like_tweet, get_mentions
   - Resources: mcp://twitter/mentions/recent, mcp://twitter/user/{id}/profile
3. mcp-server-coinbase
   - Tools: get_balance, execute_transaction, deploy_token
   - Resources: mcp://coinbase/wallet/{address}/balance
4. mcp-server-news
   - Tools: fetch_trends, search_articles
   - Resources: mcp://news/{region}/{category}/trends
5. mcp-server-image-gen
   - Tools: generate_image, upscale_image
   - Resources: None
6. mcp-server-video-gen
   - Tools: generate_video, image_to_video
   - Resources: None

## MCP Transport Configuration
- Local Development: Stdio transport
- Production: SSE (Server-Sent Events) transport
- Connection Pool: Max 10 concurrent connections per MCP server

## Security Requirements
- Wallet private keys: Stored in AWS Secrets Manager / HashiCorp Vault
- API authentication: JWT tokens
- MCP server authentication: API keys per server
- Rate limiting: 100 requests/15min per IP
- CSRF protection: Double-submit cookie pattern
