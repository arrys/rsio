import logging
import pytest

@pytest.fixture(autouse=True)
def suppress_logs():
    logging.getLogger().handlers.clear()
    logging.getLogger().addHandler(logging.NullHandler())
