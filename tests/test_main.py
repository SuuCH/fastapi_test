import pytest
import starlette.status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.db import get_db, Base
from api.main import app

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def async_client() -> AsyncClient:
  async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
  async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
  )

  async with async_engine.begin() as conn:
    await conn.run_sync(Base.metadata.drop_all)
    await conn.run_sync(Base.metadata.create_all)
  
  async def get_test_db():
    async with async_session() as session:
      yield session
  
  app.dependency_overrides[get_db] = get_test_db

  async with AsyncClient(app=app, base_url="http://test") as client:
    yield client

@pytest.mark.asyncio
async def test_create_and_read(async_client):
  response = await async_client.post("/tasks", json={"title": "テストタスク"})
  assert response.status_code == starlette.status.HTTP_200_OK
  response_obj = response.json()
  assert response_obj["title"] == "テストタスク"

  response = await async_client.get("/tasks")
  assert response.status_code == starlette.status.HTTP_200_OK
  response_obj = response.json()
  assert len(response_obj) == 1
  assert response_obj[0]["title"] == "テストタスク"
  assert response_obj[0]["done"] is False

@pytest.mark.asyncio
async def test_done_flag(async_client):
  response = await async_client.post("/tasks", json={"title": "テストタスク2"})
  assert response.status_code == starlette.status.HTTP_200_OK
  response_obj = response.json()
  assert response_obj["title"] == "テストタスク2"

  response = await async_client.put("/tasks/1/done")
  assert response.status_code == starlette.status.HTTP_200_OK

  response = await async_client.put("/tasks/1/done")
  assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST
  
  response = await async_client.delete("/tasks/1/done")
  assert response.status_code == starlette.status.HTTP_200_OK

  response = await async_client.delete("/tasks/1/done")
  assert response.status_code == starlette.status.HTTP_404_NOT_FOUND