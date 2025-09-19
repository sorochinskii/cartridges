from typing import AsyncIterator
from unittest import mock

import pytest
from api.v1.app import app
from httpx import ASGITransport, AsyncClient
from repositories.repositories import room_repository


@pytest.fixture(scope="session", autouse=True)
def room_repository_mock():
    room_repository_mock = mock.AsyncMock(spec=room_repository())
    app.dependency_overrides[room_repository] = lambda: room_repository_mock
    return room_repository_mock


@pytest.fixture
async def test_client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver") as client:
        yield client
