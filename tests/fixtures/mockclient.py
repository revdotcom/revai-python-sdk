import pytest
from src.rev_ai.apiclient import RevAiAPIClient

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


@pytest.fixture
def mockclient():
    client = RevAiAPIClient('key')
    client.session.get = MagicMock(name="mock_get")
    client.session.post = MagicMock(name="mock_post")
    return client
