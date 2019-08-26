# -*- coding: utf-8 -*-
"""Mock RevAiAPIClient for testing purposes"""

import pytest
import json
import requests
from src.rev_ai.apiclient import RevAiAPIClient


@pytest.fixture
def mock_session(mocker):
    mock_session = mocker.patch.object(requests, 'Session', autospec=True)
    mock_session.return_value.__enter__.return_value = mock_session
    return mock_session


@pytest.fixture
def make_mock_response(mocker):
    def _mock_response(url="", status=200, json_data=None, text=""):
        response = requests.Response()
        response.status_code = status
        response.reason = 'Testing'
        response.url = url
        if text:
            type(response).text = mocker.PropertyMock(return_value=text)
            type(response).content = mocker.PropertyMock(return_value=text)
        if json_data:
            response.json = mocker.Mock(return_value=json_data)
            type(response).content = mocker.PropertyMock(
                return_value=str(json_data).encode('utf-8'))
        return response
    return _mock_response
