"""High-level orchestration using CAMEL Workforce."""

from __future__ import annotations

from camel.societies.workforce import Workforce
from camel.tasks import Task
from rich.console import Console

from .agents import (
    build_preference_agent,
    build_search_agent,
    build_research_agent,
    build_planner_agent,
)

from .agents import _MODEL

console = Console()


def run_workflow() -> None:
    """Bootstrap the multi-agent workforce and run the pipeline step-by-step."""

    console.rule("[bold cyan]Launching Workforce")

    workforce = Workforce(
        description="Job-search & interview-prep pipeline",
        coordinator_agent_kwargs={"model": _MODEL, "tools": []},
        task_agent_kwargs={"model": _MODEL, "tools": []},
        new_worker_agent_kwargs={"tools": []},
    )

    workforce.add_single_agent_worker("Preference collector", build_preference_agent())
    workforce.add_single_agent_worker("Job searcher", build_search_agent())
    workforce.add_single_agent_worker("Resource finder", build_research_agent())
    workforce.add_single_agent_worker("Interview planner", build_planner_agent())

    initial_task = Task(
        content="""Collect candidate preferences by calling the 'contact_human' tool,
                   search for jobs matching the candidate's criteria using Linkup browser via 'search_linkup' tool,
                   look for resources necessary for preparation for interviews in jobs received using Brave
                   browser via 'web_search_tool' tool,
                   and craft a 14-day interview plan by pure reasoning in 'Interview planner' agent.""",
        id="0",
    )

    result_task = workforce.process_task(initial_task)

    console.rule("[bold green]Interview Plan")
    console.print(result_task.result)
