# -*- coding: utf-8 -*-
"""Unit tests for RevAiApiClient"""

import pytest
from src.rev_ai.topic_extraction_client import TopicExtractionClient
from src.rev_ai import __version__
from src.rev_ai import Transcript, Monologue, Element, TopicExtractionJob, JobStatus

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

TOKEN = 'token'
TEXT = 'Input'
JSON = Transcript([Monologue(0, [Element('text', 'hello', 0.0, 0.1, 100)])])
JOB_ID = '1'
METADATA = 'test'
CALLBACK_URL = 'https://example.com/'
CREATED_ON = '2018-05-05T23:23:22.29Z'
LANGUAGE = 'en'


class TestTopicExtractionClient:
    def test_constructor_with_success(self):
        client = TopicExtractionClient(TOKEN)

        headers = client.default_headers

        assert headers.get('User-Agent') == 'RevAi-PythonSDK/{}'.format(__version__)
        assert headers.get('Authorization') == 'Bearer {}'.format(TOKEN)
        assert client.base_url == 'https://api.rev.ai/topic_extraction/v1beta/'

    @pytest.mark.parametrize('token', [None, ''])
    def test_constructor_with_no_token(self, token):
        with pytest.raises(ValueError, match='access_token must be provided'):
            TopicExtractionClient(token)

    def test_submit_job_text_with_success(self, mock_session, make_mock_response):
        client = TopicExtractionClient(TOKEN)
        url = urljoin(client.base_url, 'jobs')
        data = {
            'id': JOB_ID,
            'status': 'in_progress',
            'created_on': CREATED_ON,
            'metadata': METADATA,
            'callback_url': CALLBACK_URL,
            'delete_after_seconds': 0,
            'language': LANGUAGE,
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.submit_job(text=TEXT,
                                metadata=METADATA,
                                callback_url=CALLBACK_URL,
                                delete_after_seconds=0,
                                language=LANGUAGE)

        assert res == TopicExtractionJob(JOB_ID,
                                         CREATED_ON,
                                         JobStatus.IN_PROGRESS,
                                         metadata=METADATA,
                                         callback_url=CALLBACK_URL,
                                         delete_after_seconds=0)
        mock_session.request.assert_called_once_with(
            "POST",
            url,
            json={
                'text': TEXT,
                'callback_url': CALLBACK_URL,
                'metadata': METADATA,
                'delete_after_seconds': 0,
                'language': LANGUAGE
            },
            headers=client.default_headers)

    def test_submit_job_json_with_success(self, mock_session, make_mock_response):
        client = TopicExtractionClient(TOKEN)
        url = urljoin(client.base_url, 'jobs')
        data = {
            'id': JOB_ID,
            'status': 'in_progress',
            'created_on': CREATED_ON,
            'metadata': METADATA,
            'callback_url': CALLBACK_URL,
            'delete_after_seconds': 0,
            'language': LANGUAGE,
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.submit_job(json=JSON,
                                metadata=METADATA,
                                callback_url=CALLBACK_URL,
                                delete_after_seconds=0,
                                language=LANGUAGE)

        assert res == TopicExtractionJob(JOB_ID,
                                         CREATED_ON,
                                         JobStatus.IN_PROGRESS,
                                         metadata=METADATA,
                                         callback_url=CALLBACK_URL,
                                         delete_after_seconds=0)
        mock_session.request.assert_called_once_with(
            "POST",
            url,
            json={
                'json': JSON.to_dict(),
                'callback_url': CALLBACK_URL,
                'metadata': METADATA,
                'delete_after_seconds': 0,
                'language': LANGUAGE
            },
            headers=client.default_headers)
