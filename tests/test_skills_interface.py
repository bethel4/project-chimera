# tests/test_skills_interface.py
import inspect

from skills.skill_trend_fetcher import TrendFetcherSkill
from skills.skill_content_generator import ContentGeneratorSkill
from skills.skill_social_publisher import SocialPublisherSkill
from skills.skill_wallet_manager import WalletManagerSkill


def _assert_has_execute_method(skill_cls):
    assert hasattr(skill_cls, "execute"), f"{skill_cls.__name__} must define execute()"
    sig = inspect.signature(skill_cls.execute)
    params = list(sig.parameters.values())
    assert len(params) == 2, "execute must accept (self, input)"
    assert params[1].annotation in (dict, inspect._empty), "input must be a dict"
    assert sig.return_annotation in (dict, inspect._empty), "execute must return a dict"


def test_all_skills_expose_execute_contract():
    """
    Spec: Task 2.3 Skill Interface Contract.
    - execute(input: dict) -> dict must exist on every skill.
    """
    for skill_cls in [
        TrendFetcherSkill,
        ContentGeneratorSkill,
        SocialPublisherSkill,
        WalletManagerSkill,
    ]:
        _assert_has_execute_method(skill_cls)


def test_skill_error_format_on_not_implemented():
    """
    Until skills are implemented, they should fail with a structured error:
    { success: False, data: None, error: { code, message } }
    """
    skills = [
        TrendFetcherSkill(),
        ContentGeneratorSkill(),
        SocialPublisherSkill(),
        WalletManagerSkill(),
    ]

    for skill in skills:
        result = skill.execute({})
        assert isinstance(result, dict)
        assert result.get("success") is False
        assert result.get("data") is None
        error = result.get("error")
        assert isinstance(error, dict)
        assert "code" in error and "message" in error