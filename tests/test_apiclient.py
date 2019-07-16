# -*- coding: utf-8 -*-
"""Unit tests for RevAiApiClient"""

import pytest
import re
from requests.exceptions import HTTPError
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai import __version__
from tests.helpers.errors import get_error_test_cases


class TestRevAiAPIClient:
    def test_constructor_with_success(self):
        token = 'token'

        client = RevAiAPIClient(token)

        headers = client.session.headers

        assert headers.get('User-Agent') == 'RevAi-PythonSDK/{}'.format(__version__)
        assert headers.get('Authorization') == 'Bearer {}'.format(token)

    @pytest.mark.parametrize('token', [None, ''])
    def test_constructor_with_no_token(self, token):
        with pytest.raises(ValueError, match='access_token must be provided'):
            RevAiAPIClient(token)

    @pytest.mark.parametrize('error', get_error_test_cases(
        ['unauthorized', 'job-not-found', 'invalid-job-state']))
    @pytest.mark.parametrize('method', ["POST", "GET", "DELETE"])
    def test_make_http_request(self, error, method, mock_client, make_mock_response):
        status = error.get('status')
        URL = RevAiAPIClient.base_url
        response = make_mock_response(url=URL, status=status, json_data=error)
        mock_client.session.request.return_value = response

        with pytest.raises(HTTPError, match= "(?=.*{})(?=.*{})".format(status, re.escape(str(error)))):
            mock_client._make_http_request(method, URL)
        mock_client.session.request.assert_called_once_with(method, URL)
