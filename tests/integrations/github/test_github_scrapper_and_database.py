import pytest
from punq import Container

from domain.entities.github import Repository
from infrastructure.repositories.github.api.scrapper import GithubRepositoryScrapper
from infrastructure.repositories.github.database.base import BaseGitHubRepository


@pytest.mark.asyncio
async def test_github_repository_scrapper_and_database(container: Container):
    github_scapper: GithubRepositoryScrapper = container.resolve(GithubRepositoryScrapper)
    repository: BaseGitHubRepository = container.resolve(BaseGitHubRepository)

    repositories: list[Repository] = await github_scapper.get_repositories()

    await repository.drop_tables()
    await repository.save_repositories(repositories)

    for repo in repositories:
        result: Repository = await repository.get_repository_by_name(name=repo.name, owner=repo.owner)

        assert isinstance(result, Repository)
        assert result.name == result.name
        assert result.owner == result.owner
        assert result.stars == result.stars
        assert result.position == result.position

        assert result.authors_commits_num_today == repo.authors_commits_num_today

    await github_scapper.close()