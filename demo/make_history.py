#!/usr/bin/env python3
"""Create a tiny, explicitly fictional Git history for a reproducible demo."""

import subprocess
import sys
from pathlib import Path


def run(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def main() -> None:
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else "demo-history").resolve()
    if repo.exists():
        raise SystemExit(f"destination exists: {repo}")
    repo.mkdir(parents=True)
    run(repo, "init", "-q")
    run(repo, "config", "user.name", "Demo Historian")
    run(repo, "config", "user.email", "demo@example.invalid")
    (repo / "legacy_cache.py").write_text(
        '"""A small fallback cache used by an imaginary service."""\n\n'
        'def read_with_fallback(cache, key, fetch):\n'
        '    """Use a cached value if fetching fails; never cache a failed fetch."""\n'
        '    try:\n'
        '        value = fetch(key)\n'
        '    except TimeoutError:\n'
        '        return cache.get(key)\n'
        '    cache[key] = value\n'
        '    return value\n', encoding="utf-8")
    run(repo, "add", "legacy_cache.py")
    run(repo, "commit", "-qm", "Add fallback read for intermittent timeouts")
    (repo / "legacy_cache.py").unlink()
    (repo / "README.md").write_text(
        "# Demo history\n\nThe old cache file was removed. This fixture does not claim a real production incident.\n",
        encoding="utf-8")
    run(repo, "add", "-A")
    run(repo, "commit", "-qm", "Remove legacy cache after switching to direct reads")
    print(repo)


if __name__ == "__main__":
    main()
