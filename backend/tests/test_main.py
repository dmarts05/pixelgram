from fastapi.testclient import TestClient

from pixelgram.__main__ import app
from pixelgram.settings import settings

client = TestClient(app)


def test_using_test_db():
    assert settings.db_uri == "sqlite+aiosqlite:///./test.db"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
