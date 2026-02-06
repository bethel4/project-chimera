# skill_content_generator

## Purpose
Generates multimodal content (text, images, video) based on a goal and persona,
using MCP tools (LLM, image-gen, video-gen).

## Input (high-level)
- `agent_id`: string
- `mode`: "text" | "image" | "video"
- `prompt`: string
- `persona_id`: string (references SOUL.md)
- `constraints`: optional object (length, style, budget tier, etc.)

## Output (high-level)
- `success`: boolean
- `data`: object with generated asset info (text, image_url, video_url, etc.)
- `error`: null or error object
