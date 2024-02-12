# Even if left empty, a conftest.py file in the base folder of your repository
# helps pytest to understand what the "top" of your project is...

import pytest

@pytest.fixture
def toplevel_fixture():
    """
    Example fixture that lives in the top level conftest.py, and returns 1
    Visible to all tests in this whole repo (because it's at the top level!)
    """
    return 1
