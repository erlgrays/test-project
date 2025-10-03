import os
import pytest
from dotenv import load_dotenv


load_dotenv()


def get_base_url() -> str:
    return os.getenv("BASE_URL", "")


@pytest.fixture(scope="session")
def base_url() -> str:
    return get_base_url()
