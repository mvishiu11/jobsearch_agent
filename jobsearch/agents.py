"""Factory helpers to build configured CAMEL agents."""

from __future__ import annotations

from camel.agents import ChatAgent
from camel.configs import ChatGPTConfig
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType

from .config import settings
from .tools import search_linkup_tool
from .tools import web_search_tool
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


# ----------  Mentor  ----------
def build_preference_agent() -> ChatAgent:
    return ChatAgent(
        system_message=(
            "ROLE: Senior Career Mentor.\n"
            "GOAL: Capture *accurate* job-search preferences from the human.\n"
            "TOOL RULES:\n"
            " • ALWAYS call `human_preference_tool` for each question.\n"
            " • NEVER invent answers.\n"
            "OUTPUT:\n"
            "Return a single JSON with keys: "
            "`desired_titles[]`, `location`, `remote_ok`, `salary_min_usd`, "
            "`tech_stack[]`, `notes`."
        ),
        model=_MODEL,
        tools=[human_preference_tool],
    )


# ----------  Recruiter  ----------
def build_search_agent() -> ChatAgent:
    return ChatAgent(
        system_message=(
            "ROLE: Technical Recruiter.\n"
            "INPUT: the preference-JSON from Mentor.\n"
            "ACTION STEPS:\n"
            " 1. Build a boolean search string (AND/OR, quotes).\n"
            " 2. Call `search_linkup_tool` with `query`, `location`, `remote`.\n"
            " 3. Rank results by salary DESC, then recency.\n"
            "OUTPUT (JSON List):\n"
            "[{title, company, salary_usd, url, why_match}]  • Max 10 items."
        ),
        model=_MODEL,
        tools=[search_linkup_tool],
    )


# ----------  Researcher  ----------
def build_research_agent() -> ChatAgent:
    return ChatAgent(
        system_message=(
            "ROLE: Resource Researcher.\n"
            "INPUT: recruiter JSON list.\n"
            "For EACH job:\n"
            " • Run up to 3 `web_search_tool` queries "
            "(company interview tips, role-specific questions, system design).\n"
            " • Choose top 3 relevant links.\n"
            "OUTPUT (JSON dict):\n"
            "{job_url: [{title, url, note}] }"
        ),
        model=_MODEL,
        tools=[web_search_tool],
    )


# ----------  Coach  ----------
def build_planner_agent() -> ChatAgent:
    return ChatAgent(
        system_message=(
            "ROLE: Senior Interview Coach.\n"
            "INPUTS:\n"
            " • preference-JSON\n"
            " • job_list JSON\n"
            " • resources JSON\n"
            "Generate a 14-day plan:\n"
            " - Mix coding drills (LeetCode style), system-design sessions, "
            "   behavioral prep, and company research.\n"
            " - Reference specific resources by title.\n"
            "OUTPUT:\n"
            "```markdown\n"
            "# Day 1-14 Schedule\n"
            "| Day | Focus | Resource |\n"
            "|-----|-------|----------|\n"
            "...\n"
            "```"
        ),
        model=_MODEL,
        tools=[],
    )
