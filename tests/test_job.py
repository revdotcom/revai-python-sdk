# -*- coding: utf-8 -*-
"""Unit tests for job endpoints"""

import json
import pytest
from requests.exceptions import HTTPError
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai.models import Job, JobStatus, JobSubmitOptions

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

JOB_ID = '1'
METADATA = 'test'
CALLBACK_URL = 'https://callback.com/'
CREATED_ON = '2018-05-05T23:23:22.29Z'
MEDIA_URL = "https://example.com/test.mp3"
JOB_ID_URL = urljoin(RevAiAPIClient.base_url, "jobs/{id}".format(id=JOB_ID))
JOB_URL = urljoin(RevAiAPIClient.base_url, "jobs")


@pytest.mark.usefixtures("mock_client", "make_mock_response")
class TestJobEndpoints():
    def test_get_job_details_with_success(self, mock_client, make_mock_response):
        status = 'transcribed'
        created_on = '2018-05-05T23:23:22.29Z'
        data = {'id': JOB_ID, 'status': status, 'created_on': created_on}
        response = make_mock_response(url=JOB_ID_URL, status=200, json_data=data)
        mock_client.session.get.return_value = response

        res = mock_client.get_job_details(JOB_ID)

        assert res == Job(JOB_ID, created_on, JobStatus.TRANSCRIBED)
        mock_client.session.get.assert_called_once_with(JOB_ID_URL)

    @pytest.mark.parametrize("id", [None, ""])
    def test_get_job_details_with_no_job_id(self, id, mock_client):
        with pytest.raises(ValueError, match='id_ must be provided'):
            mock_client.get_job_details(id)

    def test_get_job_details_with_not_authorized_error(self, mock_client, make_mock_response):
        status = 401
        data = {
            "title": "Authorization has been denied for this request",
            "status": status
        }
        response = make_mock_response(url=JOB_ID_URL, status=status, json_data=data)
        mock_client.session.get.return_value = response

        with pytest.raises(HTTPError, match=str(status)):
            mock_client.get_job_details(JOB_ID)
        mock_client.session.get.assert_called_once_with(JOB_ID_URL)

    def test_get_job_details_with_job_not_found_error(self, mock_client, make_mock_response):
        status = 404
        data = {
            "type": "https://www.rev.ai/api/v1/errors/job-not-found",
            "title": "could not find job",
            "status": 404
        }
        response = make_mock_response(url=JOB_ID_URL, status=status, json_data=data)
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
        response = make_mock_response(url=JOB_ID_URL, status=200, json_data=data)
        mock_client.session.post.return_value = response

        res = mock_client.submit_job_url(
            MEDIA_URL,
            JobSubmitOptions(metadata=METADATA, callback_url=CALLBACK_URL)
        )

        assert res == Job(JOB_ID,
                          CREATED_ON,
                          JobStatus.IN_PROGRESS,
                          metadata=METADATA,
                          callback_url=CALLBACK_URL)
        mock_client.session.post.assert_called_once_with(
            JOB_URL,
            json={
                'media_url': MEDIA_URL,
                'callback_url': CALLBACK_URL,
                'metadata': METADATA
            }
        )

    def test_submit_job_local_file_with_success(self, mocker, mock_client, make_mock_response):
        filename = "test.mp3"
        created_on = '2018-05-05T23:23:22.29Z'
        data = {
            "id": JOB_ID,
            "status": 'in_progress',
            "created_on": created_on,
            "metadata": METADATA,
            "callback_url": CALLBACK_URL
        }
        response = make_mock_response(url=JOB_ID_URL, status=200, json_data=data)
        mock_client.session.post.return_value = response

        with mocker.patch('src.rev_ai.apiclient.open', create=True)() as mock_open:
            res = mock_client.submit_job_local_file(
                filename,
                JobSubmitOptions(metadata=METADATA, callback_url=CALLBACK_URL)
            )

            assert res == Job(JOB_ID,
                              CREATED_ON,
                              JobStatus.IN_PROGRESS,
                              metadata=METADATA,
                              callback_url=CALLBACK_URL)
            mock_client.session.post.assert_called_once_with(
                JOB_URL,
                files={
                    'media': (filename, mock_open),
                    'options': (None,
                                json.dumps({'metadata': METADATA,
                                            'callback_url': CALLBACK_URL}))
                }
            )

    @pytest.mark.parametrize("url", [None, ""])
    def test_submit_job_url_with_no_media_url(self, url, mock_client):
        with pytest.raises(ValueError, match='media_url must be provided'):
            mock_client.submit_job_url(url, None)

    @pytest.mark.parametrize("filename", [None, ""])
    def test_submit_job_url_with_no_filename(self, filename, mock_client):
        with pytest.raises(ValueError, match='filename must be provided'):
            mock_client.submit_job_local_file(filename, None)

    def test_submit_job_with_bad_request_error(self, mock_client, make_mock_response):
        status = 400
        data = {
            "parameter": {
                "media_url": [
                    "The media_url field is required"
                ]
            },
            "type": "https://www.rev.ai/api/v1/errors/invalid-parameters",
            "title": "Your request parameters didn't validate",
            "status": status
        }
        response = make_mock_response(url=JOB_URL, status=status, json_data=data)
        mock_client.session.post.return_value = response

        with pytest.raises(HTTPError, match=str(status)):
            mock_client.submit_job_url(MEDIA_URL, JobSubmitOptions())
        mock_client.session.post.assert_called_once_with(
            JOB_URL, json={'media_url': MEDIA_URL, 'metadata': ''}
        )

    def test_submit_job_with_not_authorized_error(self, mock_client, make_mock_response):
        status = 401
        data = {
            "title": "Authorization has been denied for this request",
            "status": status
        }
        response = make_mock_response(url=JOB_URL, status=status, json_data=data)
        mock_client.session.post.return_value = response

        with pytest.raises(HTTPError, match=str(status)):
            mock_client.submit_job_url(MEDIA_URL, JobSubmitOptions())
        mock_client.session.post.assert_called_once_with(
            JOB_URL, json={'media_url': MEDIA_URL, 'metadata': ''}
        )

    def test_submit_job_with_insufficient_credits_error(self, mock_client, make_mock_response):
        status = 403
        data = {
            "title": "You do not have enough credits",
            "type": "https://www.rev.ai/api/v1/errors/out-of-credit",
            "detail": "You have only 60 seconds remaining",
            "current_balance": 60,
            "status": status
        }
        response = make_mock_response(url=JOB_URL, status=status, json_data=data)
        mock_client.session.post.return_value = response

        with pytest.raises(HTTPError, match=str(status)):
            mock_client.submit_job_url(MEDIA_URL, JobSubmitOptions())
        mock_client.session.post.assert_called_once_with(
            JOB_URL, json={'media_url': MEDIA_URL, 'metadata': ''}
        )
