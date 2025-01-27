from typing import Any

from domain.entities.github import (
    Repository,
    RepositoryAuthorCommitsNum,
)


def convert_repository_record_to_entity(record: dict[str, Any]) -> Repository:
    return Repository(
        name=record["name"],
        owner=record["owner"],
        position=record.get("position", 0),
        stars=record["stars"],
        watchers=record["watchers"],
        forks=record["forks"],
        language=record["language"],
    )


def convert_repository_record_to_author_stats_entity(
    records: list[dict[str, Any]],
) -> list[RepositoryAuthorCommitsNum]:

    authors_commits: list[RepositoryAuthorCommitsNum] = [
        RepositoryAuthorCommitsNum(
            author=record["author"],
            commits_num=record["commits_num"],
        )
        for record in records
        if record["author"] and record["commits_num"]
    ]

    return authors_commits
