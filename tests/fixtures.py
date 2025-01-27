from punq import Container

from bootstrap.di import _init_container


def init_dummy_container() -> Container:
    container: Container = _init_container()
    return container
