import pytest

@pytest.fixture
def example_fixture():
    """
    Example fixture that lives in /tests/conftest.py, and returns 2
    Visible to tests in this folder and below...
    """
    return 2
