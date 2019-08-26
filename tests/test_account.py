# -*- coding: utf-8 -*-
"""Unit tests for account endpoints"""

import pytest
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai.models.asynchronous import Account

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

URL = urljoin(RevAiAPIClient.base_url, 'account')


@pytest.mark.usefixtures('mock_session', 'make_mock_response')
class TestAccountEndpoints():
    def test_get_account_with_success(
            self, mock_session, make_mock_response):
        email = 'text@example.com'
        seconds = 10
        data = {'email': email, 'balance_seconds': seconds}
        response = make_mock_response(url=URL, json_data=data)
        mock_session.request.return_value = response
        client = RevAiAPIClient("token")

        res = client.get_account()

        assert res == Account(email, seconds)
        mock_session.request.assert_called_once_with("GET", URL, headers=client.default_headers)
