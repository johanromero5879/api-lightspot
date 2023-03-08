import pytest

from config import create_container


# Dependencies container
@pytest.fixture(scope="session")
def container():
    return create_container()
