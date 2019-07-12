# -*- coding: utf-8 -*-
"""Mock RevAiAPIClient for testing purposes"""

import pytest
import json
from requests import Response
from src.rev_ai.apiclient import RevAiAPIClient


@pytest.fixture
def mock_client(mocker):
    client = RevAiAPIClient('token')
    client.session.get = mocker.Mock(name='mock_get')
    client.session.post = mocker.Mock(name='mock_post')
    client.session.delete = mocker.Mock(name='mock_delete')
    return client


@pytest.fixture
def make_mock_response(mocker):
    def _mock_response(url="", status=200, json_data=None, text=""):
        response = Response()
        response.status_code = status
        response.reason = 'Testing'
        response.url = url
        if text:
            type(response).text = mocker.PropertyMock(return_value=text)
            text_bytes = json.dumps(text).encode('utf-8')
            type(response).content = mocker.PropertyMock(return_value=text_bytes)
        if json_data:
            response.json = mocker.Mock(return_value=json_data)
            json_bytes = json.dumps(json_data).encode('utf-8')
            type(response).content = mocker.PropertyMock(return_value=json_bytes)
        return response
    return _mock_response
