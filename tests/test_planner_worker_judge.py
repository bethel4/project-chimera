# tests/test_planner_worker_judge.py
import pytest

from typing import Dict, Any

# These modules do NOT exist yet – this is intentional for TDD.
from swarm.planner import Planner
from swarm.worker import Worker
from swarm.judge import Judge


def test_planner_generates_valid_task_objects(sample_persona):
    """
    Spec: FR 6.0 Planner-Worker-Judge Implementation.
    - Planner reads a high-level goal and emits Task objects matching specs/technical.md.
    """
    planner = Planner()

    goal = {
        "goal_description": "Promote the new summer fashion line in Ethiopia",
        "priority": "high",
        "persona": sample_persona,
    }

    tasks = planner.plan(goal)
    assert isinstance(tasks, list)
    assert len(tasks) > 0

    for task in tasks:
        assert isinstance(task, dict)
        assert "task_id" in task
        assert "task_type" in task
        assert "priority" in task
        assert "context" in task
        assert "status" in task
        assert task["status"] == "pending"


def test_worker_processes_tasks_and_returns_results():
    """
    Spec: FR 6.0 Worker Pool.
    - Worker.process(task) must return a Result matching the Result schema.
    """
    worker = Worker()
    fake_task: Dict[str, Any] = {
        "task_id": "test-task-1",
        "task_type": "generate_content",
        "priority": "high",
        "context": {"goal_description": "test"},
        "status": "pending",
    }

    result = worker.process(fake_task)
    assert isinstance(result, dict)
    assert "result_id" in result
    assert "task_id" in result
    assert "output" in result
    assert "confidence_score" in result
    assert 0.0 <= result["confidence_score"] <= 1.0


def test_judge_validates_and_commits_or_rejects(mock_redis):
    """
    Spec: FR 6.0 + NFR 1.0/1.1 (HITL & Confidence Thresholds).
    - Judge decides approve/reject/escalate based on confidence and policies.
    """
    judge = Judge(state_store=mock_redis)

    low_conf_result = {
        "result_id": "r1",
        "task_id": "t1",
        "output": {"type": "text", "content": "some risky content"},
        "confidence_score": 0.4,
    }

    decision_low = judge.review(low_conf_result)
    assert decision_low in ("rejected", "escalated")

    high_conf_result = {
        "result_id": "r2",
        "task_id": "t2",
        "output": {"type": "text", "content": "safe content"},
        "confidence_score": 0.95,
    }

    decision_high = judge.review(high_conf_result)
    assert decision_high == "approved"


def test_judge_enforces_occ_on_state_version():
    """
    Spec: FR 6.1 Optimistic Concurrency Control.
    - If GlobalState has changed since the worker started, commit must fail.
    """
    judge = Judge(state_store=None)  # Real impl would use Redis/DB

    result = {
        "result_id": "r3",
        "task_id": "t3",
        "output": {"type": "text", "content": "outdated content"},
        "confidence_score": 0.9,
        "state_version_at_start": 10,
    }

    # Simulate that current global state version is now 11
    current_state_version = 11

    with pytest.raises(RuntimeError):
        judge.commit(result, current_state_version=current_state_version)