import logging
import pytest

@pytest.fixture(autouse=True)
def suppress_logs():
    """Always suppress all logging output during tests."""
    logging.getLogger().handlers.clear()
    logging.getLogger().addHandler(logging.NullHandler())
