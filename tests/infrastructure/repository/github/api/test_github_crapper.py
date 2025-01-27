import pytest
from punq import Container

from infrastructure.repositories.github.api.scrapper import GithubRepositoryScrapper


@pytest.mark.asyncio
async def test_github_repository_scrapper(container: Container):
    github_scapper: GithubRepositoryScrapper = container.resolve(GithubRepositoryScrapper)
    repositries = await github_scapper.get_repositories()
    assert len(repositries) > 0, "Expected at least one repository"
    await github_scapper.close()