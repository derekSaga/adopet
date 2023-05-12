from core.config import Settings
from dotenv import load_dotenv

load_dotenv("test.env")


class TestConfig:
    def test_should_validate_meta_params(self, fxt_settings: Settings):
        assert fxt_settings.Config.case_sensitive is True
