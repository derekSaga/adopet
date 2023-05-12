import sys
from pathlib import Path

sys.path.insert(
    0,
    Path.cwd().parent.absolute().joinpath(Path.cwd().parent.absolute().name).__str__(),
)

pytest_plugins = [
    "tests.conftests.client_app_conftest",
    "tests.conftests.sqlalchemy_mocks_conftest",
    "tests.conftests.user_conftest",
    "tests.conftests.token_schema_conftest",
]
