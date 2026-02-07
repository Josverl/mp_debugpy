import pytest

pytest_plugins = [
    "fixtures.configuration",
    "fixtures.debuggee",
    "fixtures.fake_vscode",
    "fixtures.attach_server",
]
