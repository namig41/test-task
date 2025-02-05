from typing import Container

from fastapi import (
    APIRouter,
    Depends,
)

from bootstrap.di import init_container
from domain.entities.github import Repository
from infrastructure.repositories.github.api.scrapper import GithubRepositoryScrapper
from presentation.api.github.schemas import RepositoryResponseSchema


router = APIRouter(
    prefix="/github",
    tags=["Github"],
)


@router.get(
    "/{limit}",
    description="Recieve top 10 github repository",
    response_model=RepositoryResponseSchema,
)
async def get_github_repositories(
    limit: int,
    container: Container = Depends(init_container),
) -> list[RepositoryResponseSchema]:
    scrapper: GithubRepositoryScrapper = container.resolve(GithubRepositoryScrapper)

    repositories: list[Repository] = await scrapper.get_repositories(limit)

    return [
        RepositoryResponseSchema.from_entity(repository) for repository in repositories
    ]
