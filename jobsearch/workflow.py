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
from .web_agent import WebPresenterAgent
import time
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

    workforce.add_single_agent_worker("PreferenceAgent", build_preference_agent())
    workforce.add_single_agent_worker("JobSearchAgent", build_search_agent())
    workforce.add_single_agent_worker("WebAgent", build_research_agent())
    workforce.add_single_agent_worker("PlannerAgent", build_planner_agent())

    initial_task = Task(
        content="""Collect candidate preferences by calling the 'contact_human' tool,
                   search for jobs matching the candidate's criteria using Linkup browser via 'search_linkup' tool,
                   look for resources necessary for preparation for interviews in jobs received using Brave
                   browser via 'web_search_tool' tool,
                   and craft a 14-day interview plan by pure reasoning in 'PlannerAgent' agent.
                   Present all results in properly formatted markdown document, which properly summarizes
                   the information gathered by the agents and links them together. Make sure to write the
                   jobs as ranked list, sorted by salary range, DESCENDING.""",
        id="0",
    )

    result_task = workforce.process_task(initial_task)

    console.rule("[bold green]Interview Plan")
    console.print(result_task.result)

    console.print(
        "[bold cyan]\n🌐  WebPresenterAgent will be serving at http://127.0.0.1:5000\n"
        "[bold cyan]Please open this URL in your browser and wait for the agent to finish processing.\n"
        "[bold red]Attention: The agent may require your acceptance to continue the task at some point.\n"
        "[bold cyan]Press Ctrl-C to quit."
    )

    presenter = WebPresenterAgent(markdown_doc=result_task.result, model=_MODEL)
    presenter.step(presenter.get_init_message())

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[bold red]Shutting down...\n")
        console.print("[bold green]✅ Workflow finished. Goodbye!\n")
