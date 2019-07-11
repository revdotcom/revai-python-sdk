# -*- coding: utf-8 -*-
"""Unit test for testing the API failure handler"""

import pytest
from requests.exceptions import HTTPError
from src.rev_ai.apiclient import RevAiAPIClient
from tests.helpers.errors import get_error_test_cases

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

JOB_ID = '1'
URL = urljoin(RevAiAPIClient.base_url, 'jobs/{}/transcript'.format(JOB_ID))


@pytest.mark.usefixtures('mock_client', 'make_mock_response')
class TestAPIFailureHandler():
    def test_api_failure_handler_without_failure(self, mock_client, make_mock_response):
        response = make_mock_response()

        mock_client._api_failure_handler(response)

    @pytest.mark.parametrize('error', get_error_test_cases(
        ['unauthorized', 'job-not-found', 'invalid-job-state']))
    def test_api_failure_handler_with_failure(self, error, mock_client, make_mock_response):
        status = error.get('status')
        response = make_mock_response(url=URL, status=status, json_data=error, text=status)

        with pytest.raises(HTTPError, match=str(status)):
            mock_client._api_failure_handler(response)