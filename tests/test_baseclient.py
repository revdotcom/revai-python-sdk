# -*- coding: utf-8 -*-
"""Unit tests for RevAiApiClient"""

import pytest
import re
import json
from requests.exceptions import HTTPError
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai import __version__
from src.rev_ai.baseclient import BaseClient
from tests.helpers.errors import get_error_test_cases

TOKEN = "token"


class TestBaseClient:
    def test_constructor_with_success(self):
        client = BaseClient(TOKEN)

        headers = client.default_headers

        assert headers.get(
            'User-Agent') == 'RevAi-PythonSDK/{}'.format(__version__)
        assert headers.get('Authorization') == 'Bearer token'

    @pytest.mark.parametrize('token', [None, ''])
    def test_constructor_with_no_token(self, token):
        with pytest.raises(ValueError, match='access_token must be provided'):
            RevAiAPIClient(token)

    @pytest.mark.parametrize('error', get_error_test_cases(
        ['invalid-parameters', 'unauthorized', 'forbidden', 'job-not-found', 'invalid-job-state']))
    @pytest.mark.parametrize('method', ["POST", "GET", "DELETE"])
    def test_make_http_request(self, error, method, mock_session,
                               make_mock_response):
        status = error.get('status')
        URL = RevAiAPIClient.base_url
        response = make_mock_response(url=URL, status=status, json_data=error)
        mock_session.request.return_value = response
        client = RevAiAPIClient(TOKEN)

        with pytest.raises(
            HTTPError,
            match="(?=.*{})(?=.*{})".format(
                status,
                re.escape(json.dumps(error).replace('\"', '\'')))
        ):
            client._make_http_request(method, URL)
        mock_session.request.assert_called_once_with(
            method, URL,
            headers=client.default_headers
        )
