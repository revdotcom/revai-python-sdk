# -*- coding: utf-8 -*-
"""Mock RevAiAPIClient for testing purposes"""

import pytest
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
        if json_data:
            response.json = mocker.Mock(return_value=json_data)
        return response
    return _mock_response
