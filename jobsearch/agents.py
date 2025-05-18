"""Factory helpers to build configured CAMEL agents."""

from __future__ import annotations

from camel.agents import ChatAgent
from camel.configs import ChatGPTConfig
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType

from .config import settings
from .tools import search_linkup_tool
from .human import human_preference_tool

# ---------------------------------------------------------------------------
# Low‑level model factory (shared by all agents)
# ---------------------------------------------------------------------------


def _create_model():
    return ModelFactory.create(
        model_platform=getattr(ModelPlatformType, settings.model_platform.upper()),
        model_type=getattr(ModelType, settings.model_type.upper()),
        model_config_dict=ChatGPTConfig().as_dict(),
        api_key=settings.openai_api_key,
    )


_MODEL = _create_model()


# ---------------------------------------------------------------------------
# Agent builders
# ---------------------------------------------------------------------------


def build_preference_agent() -> ChatAgent:
    return ChatAgent(
        system_message=(
            "You are a career mentor. Call the 'collect_candidate_preferences' "
            "tool when you need answers; do NOT invent preferences."),
        model=_MODEL,
        tools=[human_preference_tool]
    )


def build_search_agent() -> ChatAgent:
    return ChatAgent(
        system_message=(
            "You are a recruiter. Use `search_linkup` to fetch jobs that match "
            "the candidate profile you receive."),
        model=_MODEL,
        tools=[search_linkup_tool]
    )


def build_planner_agent() -> ChatAgent:
    return ChatAgent(
        system_message=(
            "You are a senior interview coach. Craft a 14-day study plan "
            "for each supplied job posting."),
        model=_MODEL,
        tools=[]      # pure reasoning
    )
