from random import randint
from unittest import mock

from data_factory import RoomCreateFactory
from httpx import ASGITransport, AsyncClient
from main import app


async def test_get_rooms_list(
        test_client: AsyncClient,
        room_repository_mock: mock.AsyncMock):
    rooms_data = []
    for _ in range(randint(1, 5)):
        data = RoomCreateFactory.build().model_dump()
        data['id'] = str(data['id'])
        rooms_data.append(data)
    test_client = AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://testserver')
    room_repository_mock.all.return_value = rooms_data
    response = await test_client.get('/v1/rooms')
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == rooms_data
