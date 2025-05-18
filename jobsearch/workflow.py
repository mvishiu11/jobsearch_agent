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

console = Console()


def run_workflow() -> None:
    """Bootstrap the multi-agent workforce and run the pipeline step-by-step."""

    console.rule("[bold cyan]Launching Workforce")

    workforce = Workforce(
        description="Job-search & interview-prep pipeline",
        new_worker_agent_kwargs={"tools": []}
    )

    workforce.add_single_agent_worker("mentor", build_preference_agent())
    workforce.add_single_agent_worker("recruiter", build_search_agent())
    workforce.add_single_agent_worker("researcher", build_research_agent())
    workforce.add_single_agent_worker("coach", build_planner_agent())

    initial_task = Task(
        content="Collect candidate preferences, search for jobs, look for resources, and craft a 14-day interview plan",
        id="0",
    )

    result_task = workforce.process_task(initial_task)

    console.rule("[bold green]Interview Plan")
    console.print(result_task.result)
