# Technical Specification

## Agent Pattern
The system uses a Planner–Worker–Judge (Hierarchical Swarm) pattern.

## API Contract: Trend Fetcher

### Input
```json
{
  "platform": "string",
  "region": "string",
  "limit": "integer"
}
{
  "trends": [
    {
      "topic": "string",
      "score": "float",
      "source": "string"
    }
  ],
  "fetched_at": "timestamp"
}

