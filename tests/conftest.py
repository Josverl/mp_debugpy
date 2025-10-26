import pytest

pytest_plugins = [
    "fixtures.debuggee",
    "fixtures.fake_vscode",
    "fixtures.attach_server",
]
