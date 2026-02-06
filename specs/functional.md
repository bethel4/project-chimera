# Functional Requirements: User Stories

## As a Network Operator, I need to...
- Define high-level campaign goals in natural language
- Monitor fleet health and agent status in real-time
- Review aggregated analytics across all agents
- Intervene in high-level strategy when needed

## As a Human Reviewer (HITL), I need to...
- Receive escalated tasks flagged by Judge agents
- Quickly approve, reject, or edit agent-generated content
- See confidence scores and reasoning traces
- Filter by sensitive topics (Politics, Health, Financial, Legal)

## As a Chimera Agent, I need to...
- Fetch and analyze trends from news resources via MCP
- Generate multimodal content (text, images, video) using MCP tools
- Post content to social platforms via MCP tools
- Reply to comments and engage with audiences
- Manage my own crypto wallet and execute transactions
- Retrieve my long-term memories from Weaviate
- Maintain persona consistency via SOUL.md configuration

## As a Planner Agent, I need to...
- Decompose high-level goals into executable tasks
- Monitor GlobalState for campaign changes
- Generate task DAGs and push to TaskQueue
- Dynamically re-plan when context shifts

## As a Worker Agent, I need to...
- Pull tasks from TaskQueue
- Execute atomic tasks using MCP tools
- Push results to ReviewQueue
- Operate in isolation (no peer communication)

## As a Judge Agent, I need to...
- Review Worker outputs against acceptance criteria
- Score confidence (0.0-1.0) for each action
- Approve (high confidence), Escalate (medium), or Reject (low)
- Implement OCC to prevent race conditions
