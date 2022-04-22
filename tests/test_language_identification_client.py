# -*- coding: utf-8 -*-
"""Unit tests for Language Identification Client"""

import json
import pytest
from src.rev_ai.language_identification_client import LanguageIdentificationClient
from src.rev_ai import __version__
from src.rev_ai import LanguageIdentificationJob, JobStatus, \
    LanguageIdentificationResult, LanguageConfidence

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

TOKEN = 'token'
JOB_ID = '1'
METADATA = 'test'
MEDIA_URL = 'https://www.rev.ai/FTC_Sample_1.mp3'
CALLBACK_URL = 'https://example.com/'
CREATED_ON = '2018-05-05T23:23:22.29Z'
FILENAME = 'test.mp3'
TOP_LANGUAGE = 'en'
SCORE = 1


class TestLanguageIdentificationClient:
    def test_constructor_with_success(self):
        client = LanguageIdentificationClient(TOKEN)

        headers = client.default_headers

        assert headers.get('User-Agent') == 'RevAi-PythonSDK/{}'.format(__version__)
        assert headers.get('Authorization') == 'Bearer {}'.format(TOKEN)
        assert client.base_url == 'https://api.rev.ai/languageid/v1/'

    @pytest.mark.parametrize('token', [None, ''])
    def test_constructor_with_no_token(self, token):
        with pytest.raises(ValueError, match='access_token must be provided'):
            LanguageIdentificationClient(token)

    def test_submit_job_url_with_success(self, mock_session, make_mock_response):
        client = LanguageIdentificationClient(TOKEN)
        url = urljoin(client.base_url, 'jobs')
        data = {
            'id': JOB_ID,
            'created_on': CREATED_ON,
            'media_url': MEDIA_URL,
            'callback_url': CALLBACK_URL,
            'metadata': METADATA,
            'status': 'in_progress',
            'delete_after_seconds': 0
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.submit_job_url(media_url=MEDIA_URL,
                                    metadata=METADATA,
                                    callback_url=CALLBACK_URL,
                                    delete_after_seconds=0)

        assert res == LanguageIdentificationJob(JOB_ID,
                                                CREATED_ON,
                                                JobStatus.IN_PROGRESS,
                                                metadata=METADATA,
                                                callback_url=CALLBACK_URL,
                                                media_url=MEDIA_URL,
                                                delete_after_seconds=0)
        mock_session.request.assert_called_once_with(
            "POST",
            url,
            json={
                'media_url': MEDIA_URL,
                'callback_url': CALLBACK_URL,
                'metadata': METADATA,
                'delete_after_seconds': 0
            },
            headers=client.default_headers)

    def test_submit_job_local_file_with_success(self, mocker, mock_session, make_mock_response):
        client = LanguageIdentificationClient(TOKEN)
        url = urljoin(client.base_url, 'jobs')
        data = {
            'id': JOB_ID,
            'created_on': CREATED_ON,
            'callback_url': CALLBACK_URL,
            'metadata': METADATA,
            'status': 'in_progress',
            'delete_after_seconds': 0
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        with mocker.patch('src.rev_ai.language_identification_client.open', create=True)() as file:
            res = client.submit_job_local_file(FILENAME, METADATA,
                                               CALLBACK_URL, 0)

            assert res == LanguageIdentificationJob(JOB_ID,
                                                    CREATED_ON,
                                                    JobStatus.IN_PROGRESS,
                                                    metadata=METADATA,
                                                    callback_url=CALLBACK_URL,
                                                    delete_after_seconds=0)
            mock_session.request.assert_called_once_with(
                "POST",
                url,
                files={
                    'media': (FILENAME, file),
                    'options': (
                        None,
                        json.dumps({
                            'metadata': METADATA,
                            'callback_url': CALLBACK_URL,
                            'delete_after_seconds': 0
                        }, sort_keys=True)
                    )
                },
                headers=client.default_headers)

    def test_get_result_json_with_success(self, mock_session, make_mock_response):
        client = LanguageIdentificationClient(TOKEN)
        url = urljoin(client.base_url, 'jobs/{}/result'.format(JOB_ID))
        data = {
            'top_language': TOP_LANGUAGE,
            'language_confidences': [
                {
                    "language": "en",
                    "confidence": 0.907
                },
                {
                    "language": "nl",
                    "confidence": 0.023
                },
                {
                    "language": "ar",
                    "confidence": 0.023
                },
                {
                    "language": "de",
                    "confidence": 0.023
                },
                {
                    "language": "cmn",
                    "confidence": 0.023
                }
            ]
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.get_result_json(JOB_ID)

        assert res == data
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=client.default_headers)

    def test_get_result_object_with_success(self, mock_session, make_mock_response):
        client = LanguageIdentificationClient(TOKEN)
        url = urljoin(client.base_url, 'jobs/{}/result'.format(JOB_ID))
        data = {
            'top_language': TOP_LANGUAGE,
            'language_confidences': [
                {
                    "language": "en",
                    "confidence": 0.907
                },
                {
                    "language": "nl",
                    "confidence": 0.023
                },
                {
                    "language": "ar",
                    "confidence": 0.023
                },
                {
                    "language": "de",
                    "confidence": 0.023
                },
                {
                    "language": "cmn",
                    "confidence": 0.023
                }
            ]
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.get_result_object(JOB_ID)

        assert res == LanguageIdentificationResult(
            top_language=TOP_LANGUAGE,
            language_confidences=[
                LanguageConfidence(
                    language="en",
                    confidence=.907
                ),
                LanguageConfidence(
                    language="nl",
                    confidence=.023
                ),
                LanguageConfidence(
                    language="ar",
                    confidence=.023
                ),
                LanguageConfidence(
                    language="de",
                    confidence=.023
                ),
                LanguageConfidence(
                    language="cmn",
                    confidence=.023
                )
            ])
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=client.default_headers)
