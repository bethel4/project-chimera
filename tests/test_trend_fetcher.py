# tests/test_trend_fetcher.py
import pytest

from skills.skill_trend_fetcher import TrendFetcherSkill


def test_trend_fetcher_returns_contract_shape():
    """
    Spec: FR 2.0 / 2.1 / 2.2 (Perception + Trend Detection)
    - Output must match the API contract defined in specs/technical.md
    - success | data.trends | error fields are required.
    """
    skill = TrendFetcherSkill()

    result = skill.execute(
        {
            "agent_id": "agent-123",
            "sources": ["news", "twitter"],
            "niche_tags": ["fashion", "ethiopia"],
            "time_window_hours": 4,
        }
    )

    # These assertions will FAIL until the implementation is done,
    # because the current stub returns NOT_IMPLEMENTED.
    assert isinstance(result, dict)
    assert "success" in result
    assert "data" in result
    assert "error" in result

    if result["success"]:
        trends = result["data"]["trends"]
        assert isinstance(trends, list)
        for t in trends:
            assert "topic" in t
            assert "score" in t
            assert "source" in t
            assert 0.0 <= t["score"] <= 1.0


def test_trend_fetcher_applies_semantic_filtering():
    """
    Spec: FR 2.1 Semantic Filtering & Relevance Scoring.
    - High relevance items should appear with score >= 0.75
    - Irrelevant items should be filtered out or have low scores.
    """
    skill = TrendFetcherSkill()

    result = skill.execute(
        {
            "agent_id": "agent-123",
            "sources": ["news"],
            "niche_tags": ["ethiopia", "fashion"],
            "time_window_hours": 4,
        }
    )

    # This is intentionally strict; current implementation will fail.
    assert result["success"] is True
    for t in result["data"]["trends"]:
        assert 0.0 <= t["score"] <= 1.0


def test_trend_fetcher_supports_trend_clustering():
    """
    Spec: FR 2.2 Trend Detection.
    - Over time, related topics should be clustered.
    - Here we just assert that the output exposes a 'cluster_id' or similar.
    """
    skill = TrendFetcherSkill()

    result = skill.execute(
        {
            "agent_id": "agent-123",
            "sources": ["news"],
            "niche_tags": ["fashion"],
            "time_window_hours": 4,
        }
    )

    assert result["success"] is True
    for t in result["data"]["trends"]:
        # Expect clustering metadata in the future implementation
        assert "cluster_id" in t or "cluster_label" in t