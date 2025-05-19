import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_index(ac: AsyncClient) -> None:
    response = await ac.get(url="/")

    assert response.status_code == 200
