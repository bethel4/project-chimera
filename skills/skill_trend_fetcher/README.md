# skill_trend_fetcher

## Purpose
Fetches trending topics from news and social sources via MCP Resources
(e.g., `news://...`, `twitter://mentions/...`) and returns a normalized trend list.

## Input Schema (high-level)
- `agent_id`: string
- `sources`: array of strings (e.g., ["news", "twitter"])
- `niche_tags`: array of strings (e.g., ["fashion", "ethiopia"])
- `time_window_hours`: integer (e.g., 4)

## Output Schema (high-level)
- `success`: boolean
- `data.trends`: array of objects
  - `topic`: string
  - `score`: number (0.0–1.0)
  - `source`: string
- `error`: null or error object

Implementation will later call MCP resources (e.g., `news://...`) and aggregate.
