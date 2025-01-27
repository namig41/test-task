from datetime import datetime
from typing import Any
from domain.entities.github import (
    Repository,
    RepositoryAuthorCommitsNum,
)
from tools.time_utils import ts_now


def convert_commit_data_to_author_stats(
    commits: list[dict[str, Any]]
) -> list[RepositoryAuthorCommitsNum]:
    authors_commits: dict[str, Any] = {}

    today_datetime: datetime = ts_now()

    today_start: str = (
        today_datetime.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        + "Z"
    )
    today_end: str = (
        today_datetime.replace(
            hour=23, minute=59, second=59, microsecond=999999
        ).isoformat()
        + "Z"
    )

    for commit in commits:
        commit_author = commit.get("commit", {}).get("author", {})
        commit_date = commit_author.get("date", "")
        author_name = commit_author.get("name", "Unknown")

        if today_start <= commit_date <= today_end:
            authors_commits[author_name] = authors_commits.get(author_name, 0) + 1

    authors_commits_num_today: list[RepositoryAuthorCommitsNum] = [
        RepositoryAuthorCommitsNum(author=author, commits_num=commits)
        for author, commits in authors_commits.items()
    ]

    return authors_commits_num_today


def convert_repository_data_to_model(
    repo_data: dict[str, Any], position: int
) -> Repository:
    owner: str = repo_data["owner"]["login"]
    name: str = repo_data["name"]
    stars: int = repo_data["stargazers_count"]
    watchers: int = repo_data["watchers_count"]
    forks: int = repo_data["forks_count"]
    language: str = repo_data.get("language", "Unknown")

    repository: Repository = Repository(
        name=name,
        owner=owner,
        position=position,
        stars=stars,
        watchers=watchers,
        forks=forks,
        language=language,
    )

    return repository
