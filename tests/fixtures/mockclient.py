# -*- coding: utf-8 -*-
"""Mock RevAiAPIClient for testing purposes"""

import pytest
from src.rev_ai.apiclient import RevAiAPIClient


@pytest.fixture
def mockclient(mocker):
    client = RevAiAPIClient('key')
    client.session.get = mocker.Mock(name="mock_get")
    client.session.post = mocker.Mock(name="mock_post")
    return client
