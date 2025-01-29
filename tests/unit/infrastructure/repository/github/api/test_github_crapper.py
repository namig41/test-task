import pytest
from punq import Container

from domain.entities.github import Repository
from infrastructure.repositories.github.api.scrapper import GithubRepositoryScrapper


@pytest.mark.asyncio
async def test_github_repository_scrapper(container: Container):
    github_scapper: GithubRepositoryScrapper = container.resolve(GithubRepositoryScrapper)
    repositories: list[Repository] = await github_scapper.get_repositories()
    assert len(repositories) > 0
    await github_scapper.close()