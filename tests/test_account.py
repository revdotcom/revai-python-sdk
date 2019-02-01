# -*- coding: utf-8 -*-
"""Unit tests for account endpoints"""

import pytest
from requests.exceptions import HTTPError
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai.models import Account
from tests.helpers.errors import get_error_test_cases

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

URL = urljoin(RevAiAPIClient.base_url, 'account')


@pytest.mark.usefixtures('mock_client', 'make_mock_response')
class TestAccountEndpoints():
    def test_get_account_with_success(
            self, mock_client, make_mock_response):
        email = 'text@example.com'
        seconds = 10
        data = {'email': email, 'balance_seconds': seconds}
        response = make_mock_response(url=URL, json_data=data)
        mock_client.session.get.return_value = response

        res = mock_client.get_account()

        assert res == Account(email, seconds)
        mock_client.session.get.assert_called_once_with(URL)

    @pytest.mark.parametrize('error', get_error_test_cases(
        ['unauthorized']))
    def test_get_account_with_error_response(self, error, mock_client, make_mock_response):
        status = error.get('status')
        response = make_mock_response(url=URL, status=status, json_data=error)
        mock_client.session.get.return_value = response

        with pytest.raises(HTTPError, match=str(status)):
            mock_client.get_account()
        mock_client.session.get.assert_called_once_with(URL)
