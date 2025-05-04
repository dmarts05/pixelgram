from pixelgram.models.base import Base
from pixelgram.settings import settings

settings.db_uri = "sqlite+aiosqlite:///./test.db"


import pytest  # noqa: E402

from pixelgram.__main__ import app  # noqa: E402
from pixelgram.auth import current_active_user  # noqa: E402
from pixelgram.db import engine  # noqa: E402
from pixelgram.services.hf_client import get_hf_client  # noqa: E402
from pixelgram.services.supabase_client import get_supabase_client  # noqa: E402
from tests.overrides import (  # noqa: E402
    override_current_user,
    override_hf_client,
    override_supabase_client,
)


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[current_active_user] = override_current_user
    app.dependency_overrides[get_supabase_client] = override_supabase_client
    app.dependency_overrides[get_hf_client] = override_hf_client
    yield
    app.dependency_overrides = {}


@pytest.fixture(autouse=True)
async def reset_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield
