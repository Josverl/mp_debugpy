from pathlib import Path

import pytest

# fixtures to provide configuration parameters to the real fixtures


@pytest.fixture
def logToFile(request):
    # attach
    if hasattr(request, "param"):
        yield request.param
    else:
        # Default value if not parameterized
        yield False


@pytest.fixture
def source_file(request):
    # set_breakpoints
    if hasattr(request, "param"):
        yield request.param
    else:
        # Default value if not parameterized
        yield "target.py"


@pytest.fixture
def bp_lines(request):
    # set_breakpoints
    if hasattr(request, "param"):
        yield request.param
    else:
        # Default value if not parameterized
        yield from range(1, 100)  # Default to first 100 lines


# simple fixtures to provide defaults
@pytest.fixture
def local_root(request, pytestconfig: pytest.Config):
    # attach
    root_path = pytestconfig.rootpath
    if hasattr(request, "param"):
        if Path(request.param).is_absolute():
            yield Path(request.param).as_posix()
        else:
            yield (root_path / request.param).as_posix()
    else:
        # Default value if not parameterized
        yield (root_path / "tests/data").as_posix()


@pytest.fixture
def remote_root(request, pytestconfig: pytest.Config):
    # attach
    root_path = pytestconfig.rootpath
    if hasattr(request, "param"):
        if Path(request.param).is_absolute():
            yield Path(request.param).as_posix()
        else:
            yield (root_path / request.param).as_posix()
    else:
        # Default value if not parameterized
        yield (root_path / "tests/data").as_posix()


@pytest.fixture()
def tgt_module(request, pytestconfig: pytest.Config):
    """
    Fixture to provide the module name for the test.
    Can be parameterized to use different modules.
    """
    return request.param if hasattr(request, "param") else "basic"


@pytest.fixture()
def tgt_method(request, pytestconfig: pytest.Config):
    """
    Fixture to provide the method name for the test.
    Can be parameterized to use different methods.
    """
    return request.param if hasattr(request, "param") else "main"


@pytest.fixture()
def tgt_src_folder(request, pytestconfig: pytest.Config):
    """
    Fixture to provide relative source path for the target module.
    """
    root_path = Path(pytestconfig.rootpath)
    _default = (root_path / "tests/data").as_posix()
    if hasattr(request, "param"):
        if Path(request.param).is_absolute():
            yield request.param
        else:
            yield (root_path / request.param).as_posix()
    else:
        yield _default


@pytest.fixture()
def in_terminal(request):
    """
    Fixture to provide the method name for the test.
    Can be parameterized to use different methods.
    """
    # default = True
    default = False
    return request.param if hasattr(request, "param") else default


@pytest.fixture
def attach_delay(request):
    # attach
    if hasattr(request, "param"):
        yield request.param
    else:
        # Default value if not parameterized
        yield 2
