# -*- coding: utf-8 -*-
"""Unit tests for job endpoints"""

import json
import pytest
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


@pytest.mark.usefixtures("mockclient")
class TestJobEndpoints():
    def test_get_job_details_success(self, mockclient):
        status = 'transcribed'
        created_on = '2018-05-05T23:23:22.29Z'
        data = {'id': JOB_ID, 'status': status, 'created_on': created_on}
        mockclient.session.get.return_value.json.return_value = data

        res = mockclient.get_job_details(JOB_ID)

        assert res == Job(JOB_ID, created_on, JobStatus.TRANSCRIBED)
        mockclient.session.get.assert_called_once_with(
            urljoin(RevAiAPIClient.base_url, "jobs/{id}".format(id=JOB_ID))
        )

    def test_get_job_details_not_authorized_error(self, mockclient):
        data = {
            "title": "Authorization has been denied for this request",
            "status": 401
        }
        mockclient.session.get.return_value.json.return_value = data

        with pytest.raises(KeyError):
            mockclient.get_job_details(JOB_ID)

    def test_get_job_details_job_not_found_error(self, mockclient):
        data = {
            "type": "https://www.rev.ai/api/v1/errors/job-not-found",
            "title": "could not find job",
            "status": 404
        }
        mockclient.session.get.return_value.json.return_value = data

        with pytest.raises(KeyError):
            mockclient.get_job_details(JOB_ID)

    def test_submit_job_url_success(self, mockclient):
        status = 'in_progress'
        data = {
            'id': JOB_ID,
            'status': status,
            'created_on': CREATED_ON,
            'metadata': METADATA,
            'callback_url': CALLBACK_URL
        }
        mockclient.session.post.return_value.json.return_value = data

        res = mockclient.submit_job_url(
            MEDIA_URL,
            JobSubmitOptions(metadata=METADATA, callback_url=CALLBACK_URL)
        )

        assert res == Job(JOB_ID,
                          CREATED_ON,
                          JobStatus.IN_PROGRESS,
                          metadata=METADATA,
                          callback_url=CALLBACK_URL)
        mockclient.session.post.assert_called_once_with(
            urljoin(RevAiAPIClient.base_url, "jobs"),
            json={
                'media_url': MEDIA_URL,
                'callback_url': CALLBACK_URL,
                'metadata': METADATA
            }
        )

    def test_submit_job_local_file_success(self, mocker, mockclient):
        filename = "test.mp3"
        status = 'in_progress'
        created_on = '2018-05-05T23:23:22.29Z'
        data = {
            "id": JOB_ID,
            "status": status,
            "created_on": created_on,
            "metadata": METADATA,
            "callback_url": CALLBACK_URL
        }
        mockclient.session.post.return_value.json.return_value = data

        with mocker.patch('src.rev_ai.apiclient.open', create=True)() as mock_open:
            res = mockclient.submit_job_local_file(
                filename,
                JobSubmitOptions(metadata=METADATA, callback_url=CALLBACK_URL)
            )

            assert res == Job(JOB_ID,
                              CREATED_ON,
                              JobStatus.IN_PROGRESS,
                              metadata=METADATA,
                              callback_url=CALLBACK_URL)
            mockclient.session.post.assert_called_once_with(
                urljoin(RevAiAPIClient.base_url, "jobs"),
                files={
                    'media': (filename, mock_open),
                    'options': (None,
                                json.dumps({'metadata': METADATA,
                                            'callback_url': CALLBACK_URL}))
                }
            )

    def test_submit_job_bad_request_error(self, mockclient):
        data = {
            "parameter": {
                "media_url": [
                    "The media_url field is required"
                ],
                "type": "https://www.rev.ai/api/v1/errors/invalid-parameters",
                "title": "Your request parameters didn't validate",
                "status": 400
            }
        }
        mockclient.session.post.return_value.json.return_value = data

        with pytest.raises(KeyError):
            mockclient.submit_job_url(MEDIA_URL, JobSubmitOptions())

    def test_submit_job_not_authorized_error(self, mockclient):
        data = {
            "title": "Authorization has been denied for this request",
            "status": 401
        }
        mockclient.session.post.return_value.json.return_value = data

        with pytest.raises(KeyError):
            mockclient.submit_job_url(MEDIA_URL, JobSubmitOptions())

    def test_submit_job_insufficient_credits_error(self, mockclient):
        data = {
            "title": "You do not have enough credits",
            "type": "https://www.rev.ai/api/v1/errors/out-of-credit",
            "detail": "You have only 60 seconds remaining",
            "current_balance": 60,
            "status": 403
        }
        mockclient.session.post.return_value.json.return_value = data

        with pytest.raises(KeyError):
            mockclient.submit_job_url(MEDIA_URL, JobSubmitOptions())
