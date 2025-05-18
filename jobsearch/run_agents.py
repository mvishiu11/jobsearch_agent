"""Entry‑point script launched via `poetry run app`."""

from rich.console import Console
from .workflow import run_workflow


def main() -> None:  # pragma: no cover
    console = Console()
    console.print("[bold green]🚀 Jobsearch CAMEL Workforce starting up…")
    run_workflow()
    console.print("[bold green]✅ Workflow finished. Goodbye!\n")


if __name__ == "__main__":
    main()
