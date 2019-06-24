# -*- coding: utf-8 -*-

import pytest
import os.path
from requests.exceptions import HTTPError
from src.rev_ai.apiclient import RevAiAPIClient
from tests.helpers.errors import get_error_test_cases

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

JOB_ID = '1'
URL = urljoin(RevAiAPIClient.base_url, 'jobs/{}/captions'.format(JOB_ID))


@pytest.mark.usefixtures('mock_client', 'make_mock_response')
class TestCaptionEndpoint():
    def test_get_captions(self, mock_client, make_mock_response):
        data = 'Test'
        response = make_mock_response(url=URL, text=data)
        mock_client.session.get.return_value = response

        res = mock_client.get_captions(JOB_ID)

        assert res == data
        mock_client.session.get.assert_called_once_with(URL, headers={'Accept': 'application/x-subrip'})

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_captions_with_no_job_id(self, id, mock_client):
        with pytest.raises(ValueError, match='id_ must be provided'):
            mock_client.get_captions(id)

    @pytest.mark.parametrize('error', get_error_test_cases(
        ['unauthorized', 'job-not-found', 'invalid-job-state']))
    def test_get_captions_with_error_response(self, error, mock_client, make_mock_response):
        status = error.get('status')
        response = make_mock_response(url=URL, status=status, json_data=error)
        mock_client.session.get.return_value = response

        with pytest.raises(HTTPError, match=str(status)):
            mock_client.get_captions(JOB_ID)
        mock_client.session.get.assert_called_once_with(URL, headers={'Accept': 'application/x-subrip'})

    def test_get_captions_as_stream(self, mock_client, make_mock_response):
        data = 'Test'
        response = make_mock_response(url=URL, text=data)
        mock_client.session.get.return_value = response

        res = mock_client.get_captions_as_stream(JOB_ID)

        assert res.content == data
        mock_client.session.get.assert_called_once_with(URL, headers={'Accept': 'application/x-subrip'}, stream=True)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_captions_as_stream_with_no_job_id(self, id, mock_client):
        with pytest.raises(ValueError, match='id_ must be provided'):
            mock_client.get_captions_as_stream(id)

    @pytest.mark.parametrize('error', get_error_test_cases(
        ['unauthorized', 'job-not-found', 'invalid-job-state']))
    def test_get_captions_as_stream_with_error_response(self, error, mock_client, make_mock_response):
        status = error.get('status')
        response = make_mock_response(url=URL, status=status, json_data=error)
        mock_client.session.get.return_value = response

        with pytest.raises(HTTPError, match=str(status)):
            mock_client.get_captions_as_stream(JOB_ID)
        mock_client.session.get.assert_called_once_with(URL, headers={'Accept': 'application/x-subrip'}, stream=True)
