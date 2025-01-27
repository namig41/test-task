import pytest

from infrastructure.repositories.github.api.scrapper import GithubRepositoryScrapper


@pytest.mark.asyncio
async def test_github_repository_scrapper():
    github_scapper: GithubRepositoryScrapper = GithubRepositoryScrapper()