from punq import Container
import pytest

from domain.entities.github import Repository, RepositoryAuthorCommitsNum
from infrastructure.exceptions.database import RepositoryNotFoundException
from infrastructure.repositories.github.database.base import BaseGitHubRepository

mock_repository_data = {
    "name": "test-repo",
    "owner": "test-owner",
    "stars": 100,
    "watchers": 50,
    "forks": 10,
    "language": "Python",
}

mock_authors_commits = [
    RepositoryAuthorCommitsNum(author="test-author", commits_num=5)
]

@pytest.mark.asyncio
async def test_get_repository_by_name_success(container: Container):
    repository: BaseGitHubRepository = container.resolve(BaseGitHubRepository)
    
    result = await repository.get_repository_by_name(name="test-repo", owner="test-owner")

    assert isinstance(result, Repository)
    assert result.name == "test-repo"
    assert result.owner == "test-owner"
    assert result.stars == 100
    assert result.authors_commits_num_today == mock_authors_commits

@pytest.mark.asyncio
async def test_get_repository_by_name_not_found(container: Container):
    repository: BaseGitHubRepository = container.resolve(BaseGitHubRepository)
        
    with pytest.raises(RepositoryNotFoundException):
        await repository.get_repository_by_name(name="nonexistent-repo", owner="test-owner")

@pytest.mark.asyncio
async def test_save_repository(container: Container):
    repository: BaseGitHubRepository = container.resolve(BaseGitHubRepository)

    repo: Repository = Repository(**mock_repository_data)

    await repository.save_repository(repo)

    result = await repository.get_repository_by_name(name=repo.name, owner=repo.owner)

    assert isinstance(result, Repository)
    assert result.name == "test-repo"
    assert result.owner == "test-owner"
    assert result.stars == 100
    assert result.authors_commits_num_today == mock_authors_commits