from typing import Any

from domain.entities.github import (
    Repository,
    RepositoryAuthorCommitsNum,
)


def convert_repository_data_to_entity(record: dict[str, Any]) -> Repository:
    return Repository(
        name=record["name"],
        owner=record["owner"],
        position=record.get("position", 0),
        stars=record["stars"],
        watchers=record["watchers"],
        forks=record["forks"],
        language=record["language"],
    )


def convert_repository_data_to_author_stats_entity(
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


def convert_repository_entity_to_data(repository: Repository) -> dict[str, Any]:
    return {
        "name": repository.name,
        "owner": repository.owner,
        "stars": repository.stars,
        "watchers": repository.watchers,
        "forks": repository.forks,
        "language": repository.language,
    }


def convert_repository_entity_to_author_stats_data(
    repository: Repository,
) -> list[dict[str, Any]]:
    return [
        {
            "repo": repository.name,
            "author": author_commit.author,
            "commits_num": author_commit.commits_num,
        }
        for author_commit in repository.authors_commits_num_today
    ]


def convert_repositoy_entity_to_position_data(repository: Repository) -> dict[str, Any]:
    return {
        "position": repository.position,
        "repo": repository.name,
    }
