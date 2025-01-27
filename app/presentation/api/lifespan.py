from contextlib import asynccontextmanager

from fastapi import FastAPI

from punq import Container

from bootstrap.di import init_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = init_container()  # noqa

    yield
