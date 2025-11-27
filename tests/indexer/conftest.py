"""
Test fixtures for the Project Architecture Indexer.

Provides mock clients and sample data for testing.
"""

from pathlib import Path
from typing import AsyncIterator
from unittest.mock import AsyncMock, MagicMock

import pytest


# Fixture paths
FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_PROJECT_DIR = FIXTURES_DIR / "sample_project"


@pytest.fixture
def fixtures_dir() -> Path:
    """Get the fixtures directory path."""
    return FIXTURES_DIR


@pytest.fixture
def sample_project_dir() -> Path:
    """Get the sample project directory path."""
    return SAMPLE_PROJECT_DIR


@pytest.fixture
def mock_qdrant_client() -> MagicMock:
    """Create a mock Qdrant client."""
    client = MagicMock()
    client.get_collections = MagicMock(return_value=MagicMock(collections=[]))
    client.create_collection = MagicMock()
    client.upsert = MagicMock()
    client.search = MagicMock(return_value=[])
    client.scroll = MagicMock(return_value=([], None))
    client.delete = MagicMock()
    return client


@pytest.fixture
def mock_http_client() -> AsyncMock:
    """Create a mock HTTP client for embedding requests."""
    client = AsyncMock()
    client.post = AsyncMock(
        return_value=MagicMock(
            json=MagicMock(
                return_value={
                    "embeddings": [[0.1] * 1024],
                    "dimension": 1024,
                }
            )
        )
    )
    return client


@pytest.fixture
def sample_python_code() -> str:
    """Sample Python code for testing."""
    return '''"""Sample module docstring."""

def hello_world():
    """Say hello to the world."""
    print("Hello, World!")

async def fetch_data(url: str, timeout: int = 30) -> dict:
    """Fetch data from a URL.

    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds

    Returns:
        The fetched data as a dictionary
    """
    pass

class DataProcessor:
    """Process data from various sources."""

    def __init__(self, config: dict):
        """Initialize the processor."""
        self.config = config

    def process(self, data: list) -> list:
        """Process a list of data items."""
        return data

    async def async_process(self, data: list) -> list:
        """Process data asynchronously."""
        return data
'''
