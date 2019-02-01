# -*- coding: utf-8 -*-
"""Unit tests for job endpoints"""

import json
import pytest
from requests.exceptions import HTTPError
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai.models import Job, JobStatus
from tests.helpers.errors import get_error_test_cases

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

JOB_ID = '1'
METADATA = 'test'
CALLBACK_URL = 'https://callback.com/'
CREATED_ON = '2018-05-05T23:23:22.29Z'
MEDIA_URL = 'https://example.com/test.mp3'
FILENAME = 'test.mp3'
JOB_ID_URL = urljoin(RevAiAPIClient.base_url, 'jobs/{}'.format(JOB_ID))
JOBS_URL = urljoin(RevAiAPIClient.base_url, 'jobs')


@pytest.mark.usefixtures('mock_client', 'make_mock_response')
class TestJobEndpoints():
    def test_get_job_details_with_success(self, mock_client, make_mock_response):
        status = 'transcribed'
        created_on = '2018-05-05T23:23:22.29Z'
        data = {
            'id': JOB_ID,
            'status': status,
            'created_on': created_on
        }
        response = make_mock_response(url=JOB_ID_URL, json_data=data)
        mock_client.session.get.return_value = response

        res = mock_client.get_job_details(JOB_ID)

        assert res == Job(JOB_ID, created_on, JobStatus.TRANSCRIBED)
        mock_client.session.get.assert_called_once_with(JOB_ID_URL)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_job_details_with_no_job_id(self, id, mock_client):
        with pytest.raises(ValueError, match='id_ must be provided'):
            mock_client.get_job_details(id)

    @pytest.mark.parametrize('error', get_error_test_cases(
        ['unauthorized', 'job-not-found']))
    def test_get_job_details_with_error_response(self, error, mock_client, make_mock_response):
        status = error.get('status')
        response = make_mock_response(url=JOB_ID_URL, status=status, json_data=error)
        mock_client.session.get.return_value = response

        with pytest.raises(HTTPError, match=str(status)):
            mock_client.get_job_details(JOB_ID)
        mock_client.session.get.assert_called_once_with(JOB_ID_URL)

    def test_submit_job_url_with_success(self, mock_client, make_mock_response):
        data = {
            'id': JOB_ID,
            'status': 'in_progress',
            'created_on': CREATED_ON,
            'metadata': METADATA,
            'callback_url': CALLBACK_URL
        }
        response = make_mock_response(url=JOB_ID_URL, json_data=data)
        mock_client.session.post.return_value = response

        res = mock_client.submit_job_url(MEDIA_URL, METADATA, CALLBACK_URL)

        assert res == Job(JOB_ID,
                          CREATED_ON,
                          JobStatus.IN_PROGRESS,
                          metadata=METADATA,
                          callback_url=CALLBACK_URL)
        mock_client.session.post.assert_called_once_with(
            JOBS_URL,
            json={
                'media_url': MEDIA_URL,
                'callback_url': CALLBACK_URL,
                'metadata': METADATA
            })

    @pytest.mark.parametrize('url', [None, ''])
    def test_submit_job_url_with_no_media_url(self, url, mock_client):
        with pytest.raises(ValueError, match='media_url must be provided'):
            mock_client.submit_job_url(url)

    @pytest.mark.parametrize('error', get_error_test_cases(
        ['invalid-parameters', 'unauthorized', 'out-of-credit']))
    def test_submit_job_url_with_error_response(self, error, mock_client, make_mock_response):
        status = error.get('status')
        response = make_mock_response(url=JOBS_URL, status=status, json_data=error)
        mock_client.session.post.return_value = response

        with pytest.raises(HTTPError, match=str(status)):
            mock_client.submit_job_url(MEDIA_URL)
        mock_client.session.post.assert_called_once_with(JOBS_URL, json={'media_url': MEDIA_URL})

    def test_submit_job_local_file_with_success(self, mocker, mock_client, make_mock_response):
        created_on = '2018-05-05T23:23:22.29Z'
        data = {
            'id': JOB_ID,
            'status': 'in_progress',
            'created_on': created_on,
            'metadata': METADATA,
            'callback_url': CALLBACK_URL
        }
        response = make_mock_response(url=JOB_ID_URL, json_data=data)
        mock_client.session.post.return_value = response

        with mocker.patch('src.rev_ai.apiclient.open', create=True)() as file:
            res = mock_client.submit_job_local_file(FILENAME, METADATA, CALLBACK_URL)

            assert res == Job(JOB_ID,
                              CREATED_ON,
                              JobStatus.IN_PROGRESS,
                              metadata=METADATA,
                              callback_url=CALLBACK_URL)
            mock_client.session.post.assert_called_once_with(
                JOBS_URL,
                files={
                    'media': (FILENAME, file),
                    'options': (
                        None,
                        json.dumps({
                            'metadata': METADATA,
                            'callback_url': CALLBACK_URL
                        })
                    )
                })

    @pytest.mark.parametrize('filename', [None, ''])
    def test_submit_job_url_with_no_filename(self, filename, mock_client):
        with pytest.raises(ValueError, match='filename must be provided'):
            mock_client.submit_job_local_file(filename, None)

    @pytest.mark.parametrize('error', get_error_test_cases(
        ['invalid-parameters', 'unauthorized', 'out-of-credit']))
    def test_submit_job_local_file_with_error_response(
            self, error, mocker, mock_client, make_mock_response):
        status = error.get('status')
        response = make_mock_response(url=JOBS_URL, status=status, json_data=error)
        mock_client.session.post.return_value = response

        with mocker.patch('src.rev_ai.apiclient.open', create=True)() as file:
            with pytest.raises(HTTPError, match=str(status)):
                mock_client.submit_job_local_file(FILENAME)
            mock_client.session.post.assert_called_once_with(
                JOBS_URL, files={'media': (FILENAME, file), 'options': (None, '{}')})

    def test_delete_job_success(self, mock_client, make_mock_response):
        response = make_mock_response(url=JOB_ID_URL, status=204)
        mock_client.session.delete.return_value = response

        res = mock_client.delete_job(JOB_ID)

        assert res is None
        mock_client.session.delete.assert_called_once_with(JOB_ID_URL)

    @pytest.mark.parametrize('error', get_error_test_cases(
        ['unauthorized', 'job-not-found', 'invalid-job-state']))
    def test_delete_job_with_error_response(
            self, error, mocker, mock_client, make_mock_response):
        status = error.get('status')
        response = make_mock_response(url=JOB_ID_URL, status=status, json_data=error)
        mock_client.session.delete.return_value = response

        with pytest.raises(HTTPError, match=str(status)):
            mock_client.delete_job(JOB_ID)
        mock_client.session.delete.assert_called_once_with(JOB_ID_URL)

    @pytest.mark.parametrize('id', [None, ''])
    def test_delete_job_with_no_id(self, id, mock_client):
        with pytest.raises(ValueError, match='id_ must be provided'):
            mock_client.delete_job(id)
