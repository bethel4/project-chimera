# skill_wallet_manager

## Purpose
Wraps Coinbase AgentKit / MCP tools to manage non-custodial wallets:
- get_balance
- native_transfer / ERC-20 transfers
- basic budget checks (CFO policies handled by Judge)

## Input (high-level)
- `agent_id`: string
- `action`: "get_balance" | "send_payment"
- For "send_payment":
  - `to_address`: string
  - `amount_usdc`: number

## Output (high-level)
- `success`: boolean
- `data`: object (balance info or tx hash)
- `error`: null or error object
