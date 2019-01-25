# -*- coding: utf-8 -*-
"""Unit tests for transcript endpoints"""

import pytest
from src.rev_ai.models import Transcript
from src.rev_ai.apiclient import RevAiAPIClient

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

JOB_ID = '1'


@pytest.mark.usefixtures("mockclient")
class TestTranscriptEndpoints():
    def test_get_transcript_test_success(self, mockclient):
        data = "Hello"
        mockclient.session.get.return_value.text = data

        res = mockclient.get_transcript_text(JOB_ID)

        assert res == data
        mockclient.session.get.assert_called_once_with(
            urljoin(
                RevAiAPIClient.base_url,
                'jobs/{id}/transcript'.format(id=JOB_ID)
            ),
            headers={'Accept': 'text/plain'}
        )

    def test_get_transcript_object_success(self, mockclient):
        data = {
            "monologues": [
                {
                    "speaker": 1,
                    "elements": [
                        {
                            "type": "text",
                            "value": "Hello",
                            "ts": 0.75,
                            "ts_end": 1.25,
                            "confidence": 0.85
                        }
                    ]
                }
            ]
        }
        mockclient.session.get.return_value.json.return_value = data

        res = mockclient.get_transcript_object(JOB_ID)

        assert isinstance(res, Transcript)
        assert len(res.monologues) == 1
        assert res.monologues[0].speaker == 1
        assert len(res.monologues[0].elements) == 1
        assert res.monologues[0].elements[0].value == "Hello"
        mockclient.session.get.assert_called_once_with(
            urljoin(
                RevAiAPIClient.base_url,
                'jobs/{id}/transcript'.format(id=JOB_ID)
            ),
            headers={'Accept': 'application/vnd.rev.transcript.v1.0+json'}
        )

    def test_get_transcript_not_authorized_error(self, mockclient):
        data = {
            "title": "Authorization has been denied for this request",
            "status": 401
        }
        mockclient.session.get.return_value.json.return_value = data

        res = mockclient.get_transcript_object(JOB_ID)

        assert isinstance(res, Transcript)
        assert len(res.monologues) == 0
        mockclient.session.get.assert_called_once_with(
            urljoin(
                RevAiAPIClient.base_url,
                'jobs/{id}/transcript'.format(id=JOB_ID)
            ),
            headers={'Accept': 'application/vnd.rev.transcript.v1.0+json'}
        )

    def test_get_transcript_job_not_found_error(self, mockclient):
        data = {
            "type": "https://www.rev.ai/api/v1/errors/job-not-found",
            "title": "could not find job",
            "status": 404
        }
        mockclient.session.get.return_value.json.return_value = data

        res = mockclient.get_transcript_object(JOB_ID)

        assert isinstance(res, Transcript)
        assert len(res.monologues) == 0
        mockclient.session.get.assert_called_once_with(
            urljoin(
                RevAiAPIClient.base_url,
                'jobs/{id}/transcript'.format(id=JOB_ID)
            ),
            headers={'Accept': 'application/vnd.rev.transcript.v1.0+json'}
        )

    def test_get_transcript_invalid_job_state_error(self, mockclient):
        data = {
            "allowed_values": [
                "transcribed"
            ],
            "current_value": "in_progress",
            "type": "https://rev.ai/api/v1/errors/invalid-job-state",
            "title": "Job is in invalid state",
            "detail": "Job is in invalid state to obtain the transcript",
            "status": 409
        }
        mockclient.session.get.return_value.json.return_value = data

        res = mockclient.get_transcript_object(JOB_ID)

        assert isinstance(res, Transcript)
        assert len(res.monologues) == 0
        mockclient.session.get.assert_called_once_with(
            urljoin(
                RevAiAPIClient.base_url,
                'jobs/{id}/transcript'.format(id=JOB_ID)
            ),
            headers={'Accept': 'application/vnd.rev.transcript.v1.0+json'}
        )
