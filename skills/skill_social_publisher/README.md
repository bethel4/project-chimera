# skill_social_publisher

## Purpose
Publishes prepared content to social platforms via MCP tools
(e.g., twitter.post_tweet, instagram.publish_media).

## Input (high-level)
- `agent_id`: string
- `platform`: "twitter" | "instagram" | "threads" | "tiktok"
- `text_content`: string
- `media_urls`: array of strings (optional)
- `disclosure_level`: "automated" | "assisted" | "none"

## Output (high-level)
- `success`: boolean
- `data.post_id`: string or null
- `error`: null or error object
