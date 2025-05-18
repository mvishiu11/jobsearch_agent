"""Factory helpers to build configured CAMEL agents."""

from __future__ import annotations

from camel.agents import ChatAgent
from camel.configs import ChatGPTConfig
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType

from .config import settings
from .tools import search_linkup_tool
from .tools import web_search_tool
from .human import human_tool

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
            """Gather candidate preferences from the candidate
            by calling the 'contact_human' tool. Do NOT invent preferences. Stop when you have information about 
            candidate's preferences regarding role, location and remote work preference."""),
        model=_MODEL,
        tools=[human_tool]
    )


# ----------  Recruiter  ----------
def build_search_agent() -> ChatAgent:
    return ChatAgent(
        system_message=(
            "Use `search_linkup_tool` to fetch jobs that match"
            "the candidate profile you receive. Stop when you have information about "
            "matching jobs."
            "Make sure to look for specific job titles, company names, and job URLs."
            "OUTPUT: A list of no less than 5 and no more than 10 jobs, with job titles, company names, and job URLs."),
        model=_MODEL,
        tools=[search_linkup_tool]
    )


# ----------  Researcher  ----------
def build_research_agent() -> ChatAgent:
    return ChatAgent(
        system_message=(
            "Use `web_search_tool` to fetch information "
            "about interview resources necessary for preparation for interviews in jobs received. "
            "Stop when you have a at least 5 resources."
            "OUTPUT: A list of no less than 5 and no more than 10 resources, "
            "with resource titles, descriptions, and URLs."),
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
