import asyncio
from typing import AsyncIterator, Generator

import pytest
from httpx import ASGITransport, AsyncClient
from main import app


@pytest.fixture
async def test_client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://testserver') as client:
        yield client
