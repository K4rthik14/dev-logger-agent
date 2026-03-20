import os
from datetime import datetime, date
from typing import Optional

from git import Repo, InvalidGitRepositoryError
from langchain_core.tools import tool

_repo: Optional[Repo] = None
_repo_path: str = ""


def init_repo(path: str) -> Repo:
    global _repo, _repo_path
    try:
        _repo = Repo(path, search_parent_directories=True)
        _repo_path = _repo.working_tree_dir
        return _repo
    except InvalidGitRepositoryError:
        raise ValueError(f"No git repository found at: {path}")


@tool
def get_repo_info() -> str:
    """Get basic repo metadata: name, current branch, remote URL, total commits today. Always call this first."""
    if _repo is None:
        return "Error: Repository not initialized."
    try:
        name = os.path.basename(_repo_path)
        branch = _repo.active_branch.name
        remotes = [r.url for r in _repo.remotes] if _repo.remotes else ["(no remote)"]
        today_commits = len(list(_repo.iter_commits(after=f"{date.today()} 00:00:00")))
        return (
            f"Repo: {name}\n"
            f"Branch: {branch}\n"
            f"Remote: {remotes[0]}\n"
            f"Commits today: {today_commits}"
        )
    except Exception as e:
        return f"Error: {e}"


@tool
def get_commits(since_date: str = "") -> str:
    """Fetch git commits from today (or a specific date YYYY-MM-DD). Returns hashes, authors, timestamps, messages."""
    if _repo is None:
        return "Error: Repository not initialized."
    target_date = since_date.strip() if since_date else str(date.today())
    try:
        commits = list(_repo.iter_commits(after=f"{target_date} 00:00:00"))
    except Exception as e:
        return f"Error fetching commits: {e}"
    if not commits:
        return f"No commits found for {target_date}."
    lines = [f"Found {len(commits)} commit(s) on {target_date}:\n"]
    for c in commits:
        ts = datetime.fromtimestamp(c.committed_date).strftime("%H:%M")
        lines.append(f"- [{c.hexsha[:7]}] {ts} | {c.author.name}: {c.message.strip()}")
    return "\n".join(lines)


@tool
def list_changed_files(since_date: str = "") -> str:
    """List all files changed across today's commits (or a given YYYY-MM-DD date)."""
    if _repo is None:
        return "Error: Repository not initialized."
    target_date = since_date.strip() if since_date else str(date.today())
    try:
        commits = list(_repo.iter_commits(after=f"{target_date} 00:00:00"))
    except Exception as e:
        return f"Error: {e}"
    if not commits:
        return f"No commits found for {target_date}."
    all_files: set[str] = set()
    for c in commits:
        if c.parents:
            for d in c.parents[0].diff(c):
                if d.b_path:
                    all_files.add(d.b_path)
    if not all_files:
        return "No file changes detected."
    sorted_files = sorted(all_files)
    return f"Files changed on {target_date} ({len(sorted_files)} total):\n" + "\n".join(
        f"  - {f}" for f in sorted_files
    )


@tool
def get_diff(commit_sha: str = "HEAD") -> str:
    """Get the code diff for a specific commit SHA (default: HEAD). Returns changed files and additions/deletions."""
    if _repo is None:
        return "Error: Repository not initialized."
    try:
        commit = _repo.commit(commit_sha)
        if not commit.parents:
            return f"Commit {commit_sha[:7]} is the initial commit — no diff available."
        diffs = commit.parents[0].diff(commit, create_patch=True)
        if not diffs:
            return "No file changes found in this commit."
        MAX_CHARS_PER_FILE = 1500
        output = [f"Diff for commit {commit.hexsha[:7]} — {commit.message.strip()}\n"]
        for d in diffs:
            path = d.b_path or d.a_path
            try:
                patch = d.diff.decode("utf-8", errors="ignore")
            except Exception:
                patch = "[binary file]"
            lines_added = patch.count("\n+")
            lines_removed = patch.count("\n-")
            output.append(f"\n📄 {path}  (+{lines_added} / -{lines_removed})")
            output.append(patch[:MAX_CHARS_PER_FILE])
            if len(patch) > MAX_CHARS_PER_FILE:
                output.append("... [truncated]")
        return "\n".join(output)
    except Exception as e:
        return f"Error getting diff for {commit_sha}: {e}"


@tool
def read_file(file_path: str) -> str:
    """Read the current contents of a file in the repo. Provide path relative to repo root e.g. 'src/main.py'."""
    if _repo is None or not _repo_path:
        return "Error: Repository not initialized."
    full_path = os.path.join(_repo_path, file_path.strip())
    if not os.path.exists(full_path):
        return f"File not found: {file_path}"
    if not os.path.isfile(full_path):
        return f"Path is not a file: {file_path}"
    try:
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        MAX_CHARS = 3000
        if len(content) > MAX_CHARS:
            return content[:MAX_CHARS] + "\n... [file truncated]"
        return content
    except Exception as e:
        return f"Error reading file: {e}"


ALL_TOOLS = [get_repo_info, get_commits, list_changed_files, get_diff, read_file]