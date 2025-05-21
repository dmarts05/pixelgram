from pixelgram.models.user import User
from pixelgram.settings import Settings, settings
from tests.utils import get_test_user


async def override_current_user() -> User:
    return get_test_user()


def override_small_image_size_settings() -> Settings:
    overriden_settings = settings.model_copy()
    overriden_settings.max_img_mb_size = 0.0001
    return overriden_settings


class MockHFClient:
    async def generate_caption(self, img_bytes):
        return "Mock caption"


async def override_hf_client() -> MockHFClient:
    return MockHFClient()


class FailMockHFClient:
    async def generate_caption(self, img_bytes):
        return None


def override_fail_hf_client():
    return FailMockHFClient()


class MockSupabaseClient:
    async def upload(self, img):
        return "https://mockstorage.com/image.png"

    async def delete(self, file_id: str) -> None:
        pass


async def override_supabase_client() -> MockSupabaseClient:
    return MockSupabaseClient()
