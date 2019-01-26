# -*- coding: utf-8 -*-
"""Unit tests for account endpoints"""

import pytest
from requests.exceptions import HTTPError
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai.models import Account

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

URL = urljoin(RevAiAPIClient.base_url, "account")


@pytest.mark.usefixtures("mock_client", "make_mock_response")
class TestAccountEndpoints():
    def test_get_account_with_success(self, mock_client, make_mock_response):
        email = "text@example.com"
        seconds = 10
        data = {"email": email, "balance_seconds": seconds}
        response = make_mock_response(url=URL, status=200, json_data=data)
        mock_client.session.get.return_value = response

        res = mock_client.get_account()

        assert res == Account(email, seconds)
        mock_client.session.get.assert_called_once_with(URL)

    def test_get_account_with_not_authorized_error(self, mock_client, make_mock_response):
        status = 401
        data = {
            "title": "Authorization has been denied for this request",
            "status": status
        }
        response = make_mock_response(url=URL, status=status, json_data=data)
        mock_client.session.get.return_value = response

        with pytest.raises(HTTPError, match=str(status)):
            mock_client.get_account()
        mock_client.session.get.assert_called_once_with(URL)
