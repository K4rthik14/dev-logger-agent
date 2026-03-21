import os
from datetime import date, timedelta, datetime
from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

app = typer.Typer(help="Dev Logger Agent — auto-generate daily dev logs from git history.")
console = Console()


def date_range(start: str, end: str):
    """Yield all dates from start to end inclusive."""
    s = datetime.strptime(start, "%Y-%m-%d").date()
    e = datetime.strptime(end, "%Y-%m-%d").date()
    current = s
    while current <= e:
        yield str(current)
        current += timedelta(days=1)


@app.command()
def log(
    path: str = typer.Option(".", "--path", "-p", help="Path to the git repo"),
    log_date: str = typer.Option("", "--date", "-d", help="Date YYYY-MM-DD (default: today)"),
    since: str = typer.Option("", "--since", "-s", help="Generate logs from this date to today YYYY-MM-DD"),
    save: bool = typer.Option(True, "--save/--no-save", help="Save log to ./logs/"),
    output_dir: str = typer.Option("logs", "--output", "-o", help="Directory to save logs"),
    model: str = typer.Option("llama-3.3-70b-versatile", "--model", "-m", help="Groq model"),
):
    """Generate a structured dev log for a git repository."""
    repo_path = str(Path(path).resolve())

    # Build list of dates to process
    if since:
        dates = list(date_range(since, str(date.today())))
    else:
        dates = [log_date or str(date.today())]

    console.print(Panel(
        f"[bold cyan]Dev Logger Agent[/bold cyan]\n"
        f"Repo: [yellow]{repo_path}[/yellow]\n"
        f"Dates: [green]{dates[0]} → {dates[-1]}[/green] ({len(dates)} day(s))\n"
        f"Model: [dim]{model}[/dim]",
        title="🤖 Starting", border_style="cyan"
    ))

    try:
        from dev_logger.agent import run_agent

        for target_date in dates:
            console.print(f"\n[bold]📅 Processing {target_date}...[/bold]")
            log_content = run_agent(repo_path=repo_path, log_date=target_date)

            console.print(Panel(Markdown(log_content), title=f"📋 {target_date}", border_style="green"))

            if save:
                log_dir = Path(output_dir)
                log_dir.mkdir(parents=True, exist_ok=True)
                log_file = log_dir / f"{target_date}.md"
                with open(log_file, "w", encoding="utf-8") as f:
                    f.write(log_content)
                console.print(f"[bold green]✅ Saved:[/bold green] {log_file}")

    except EnvironmentError as e:
        console.print(f"\n[bold red]❌ Config Error:[/bold red] {e}")
        raise typer.Exit(1)
    except ValueError as e:
        console.print(f"\n[bold red]❌ Repo Error:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()import os
from datetime import date, timedelta, datetime
from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

app = typer.Typer(help="Dev Logger Agent — auto-generate daily dev logs from git history.")
console = Console()


def date_range(start: str, end: str):
    """Yield all dates from start to end inclusive."""
    s = datetime.strptime(start, "%Y-%m-%d").date()
    e = datetime.strptime(end, "%Y-%m-%d").date()
    current = s
    while current <= e:
        yield str(current)
        current += timedelta(days=1)


@app.command()
def log(
    path: str = typer.Option(".", "--path", "-p", help="Path to the git repo"),
    log_date: str = typer.Option("", "--date", "-d", help="Date YYYY-MM-DD (default: today)"),
    since: str = typer.Option("", "--since", "-s", help="Generate logs from this date to today YYYY-MM-DD"),
    save: bool = typer.Option(True, "--save/--no-save", help="Save log to ./logs/"),
    output_dir: str = typer.Option("logs", "--output", "-o", help="Directory to save logs"),
    model: str = typer.Option("llama-3.3-70b-versatile", "--model", "-m", help="Groq model"),
):
    """Generate a structured dev log for a git repository."""
    repo_path = str(Path(path).resolve())

    # Build list of dates to process
    if since:
        dates = list(date_range(since, str(date.today())))
    else:
        dates = [log_date or str(date.today())]

    console.print(Panel(
        f"[bold cyan]Dev Logger Agent[/bold cyan]\n"
        f"Repo: [yellow]{repo_path}[/yellow]\n"
        f"Dates: [green]{dates[0]} → {dates[-1]}[/green] ({len(dates)} day(s))\n"
        f"Model: [dim]{model}[/dim]",
        title="🤖 Starting", border_style="cyan"
    ))

    try:
        from dev_logger.agent import run_agent

        for target_date in dates:
            console.print(f"\n[bold]📅 Processing {target_date}...[/bold]")
            log_content = run_agent(repo_path=repo_path, log_date=target_date)

            console.print(Panel(Markdown(log_content), title=f"📋 {target_date}", border_style="green"))

            if save:
                log_dir = Path(output_dir)
                log_dir.mkdir(parents=True, exist_ok=True)
                log_file = log_dir / f"{target_date}.md"
                with open(log_file, "w", encoding="utf-8") as f:
                    f.write(log_content)
                console.print(f"[bold green]✅ Saved:[/bold green] {log_file}")

    except EnvironmentError as e:
        console.print(f"\n[bold red]❌ Config Error:[/bold red] {e}")
        raise typer.Exit(1)
    except ValueError as e:
        console.print(f"\n[bold red]❌ Repo Error:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()