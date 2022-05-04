# -*- coding: utf-8 -*-
"""Unit tests for TopicExtractionClient"""

import pytest

from src.rev_ai.topic_extraction_client import TopicExtractionClient
from src.rev_ai import __version__
from src.rev_ai import Transcript, Monologue, Element, TopicExtractionJob, JobStatus, \
    TopicExtractionResult, Topic, Informant, CustomerUrlData

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

TOKEN = 'token'
TEXT = 'Input'
JSON = Transcript([Monologue(0, [Element('text', 'hello', 0.0, 0.1, 100)])])
JOB_ID = '1'
METADATA = 'test'
NOTIFICATION_URL = 'https://example.com/'
NOTIFICATION_AUTH = 'headers'
CREATED_ON = '2018-05-05T23:23:22.29Z'
LANGUAGE = 'en'
TOPIC_NAME = 'random'
SCORE = 1
INFORMANT_CONTENT = 'random words'
INFORMANT_OFFSET = 0
INFORMANT_LENGTH = 12
THRESHOLD = .3

NOTIFICATION_CONFIG = CustomerUrlData(NOTIFICATION_URL, NOTIFICATION_AUTH)


class TestTopicExtractionClient:
    def test_constructor_with_success(self):
        client = TopicExtractionClient(TOKEN)

        headers = client.default_headers

        assert headers.get('User-Agent') == 'RevAi-PythonSDK/{}'.format(__version__)
        assert headers.get('Authorization') == 'Bearer {}'.format(TOKEN)
        assert client.base_url == 'https://api.rev.ai/topic_extraction/v1/'

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
            'delete_after_seconds': 0,
            'language': LANGUAGE,
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.submit_job_from_text(text=TEXT,
                                          metadata=METADATA,
                                          callback_url=NOTIFICATION_URL,
                                          delete_after_seconds=0,
                                          language=LANGUAGE)

        assert res == TopicExtractionJob(JOB_ID,
                                         CREATED_ON,
                                         JobStatus.IN_PROGRESS,
                                         metadata=METADATA,
                                         delete_after_seconds=0)
        mock_session.request.assert_called_once_with(
            "POST",
            url,
            json={
                'text': TEXT,
                'callback_url': NOTIFICATION_URL,
                'metadata': METADATA,
                'delete_after_seconds': 0,
                'language': LANGUAGE
            },
            headers=client.default_headers)

    def test_submit_job_text_auth_options_with_success(self, mock_session, make_mock_response):
        client = TopicExtractionClient(TOKEN)
        url = urljoin(client.base_url, 'jobs')
        data = {
            'id': JOB_ID,
            'status': 'in_progress',
            'created_on': CREATED_ON,
            'metadata': METADATA,
            'delete_after_seconds': 0,
            'language': LANGUAGE,
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.submit_job_from_text(text=TEXT,
                                          metadata=METADATA,
                                          notification_config=NOTIFICATION_CONFIG,
                                          delete_after_seconds=0,
                                          language=LANGUAGE)

        assert res == TopicExtractionJob(JOB_ID,
                                         CREATED_ON,
                                         JobStatus.IN_PROGRESS,
                                         metadata=METADATA,
                                         delete_after_seconds=0)
        mock_session.request.assert_called_once_with(
            "POST",
            url,
            json={
                'text': TEXT,
                'notification_config': {'url': NOTIFICATION_URL, 'auth_headers': NOTIFICATION_AUTH},
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
            'delete_after_seconds': 0,
            'language': LANGUAGE,
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.submit_job_from_transcript(transcript=JSON,
                                                metadata=METADATA,
                                                callback_url=NOTIFICATION_URL,
                                                delete_after_seconds=0,
                                                language=LANGUAGE)

        assert res == TopicExtractionJob(JOB_ID,
                                         CREATED_ON,
                                         JobStatus.IN_PROGRESS,
                                         metadata=METADATA,
                                         delete_after_seconds=0)
        mock_session.request.assert_called_once_with(
            "POST",
            url,
            json={
                'json': JSON.to_dict(),
                'callback_url': NOTIFICATION_URL,
                'metadata': METADATA,
                'delete_after_seconds': 0,
                'language': LANGUAGE
            },
            headers=client.default_headers)

    def test_submit_job_json_auth_options_with_success(self, mock_session, make_mock_response):
        client = TopicExtractionClient(TOKEN)
        url = urljoin(client.base_url, 'jobs')
        data = {
            'id': JOB_ID,
            'status': 'in_progress',
            'created_on': CREATED_ON,
            'metadata': METADATA,
            'delete_after_seconds': 0,
            'language': LANGUAGE,
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.submit_job_from_transcript(transcript=JSON,
                                                metadata=METADATA,
                                                notification_config=NOTIFICATION_CONFIG,
                                                delete_after_seconds=0,
                                                language=LANGUAGE)

        assert res == TopicExtractionJob(JOB_ID,
                                         CREATED_ON,
                                         JobStatus.IN_PROGRESS,
                                         metadata=METADATA,
                                         delete_after_seconds=0)
        mock_session.request.assert_called_once_with(
            "POST",
            url,
            json={
                'json': JSON.to_dict(),
                'notification_config': {'url': NOTIFICATION_URL, 'auth_headers': NOTIFICATION_AUTH},
                'metadata': METADATA,
                'delete_after_seconds': 0,
                'language': LANGUAGE
            },
            headers=client.default_headers)

    def test_get_result_json_with_success(self, mock_session, make_mock_response):
        client = TopicExtractionClient(TOKEN)
        url = urljoin(client.base_url, 'jobs/{}/result?'.format(JOB_ID))
        data = {
            'topics': [
                {
                    'topic_name': TOPIC_NAME,
                    'score': SCORE,
                    'informants': [
                        {
                            'content': INFORMANT_CONTENT,
                            'offset': INFORMANT_OFFSET,
                            'length': INFORMANT_LENGTH
                        }
                    ]
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

    def test_get_result_json_with_threshold_with_success(self, mock_session, make_mock_response):
        client = TopicExtractionClient(TOKEN)
        url = urljoin(client.base_url, 'jobs/{0}/result?threshold={1}'.format(JOB_ID, THRESHOLD))
        data = {
            'topics': [
                {
                    'topic_name': TOPIC_NAME,
                    'score': SCORE,
                    'informants': [
                        {
                            'content': INFORMANT_CONTENT,
                            'offset': INFORMANT_OFFSET,
                            'length': INFORMANT_LENGTH
                        }
                    ]
                }
            ]
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.get_result_json(JOB_ID, THRESHOLD)

        assert res == data
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=client.default_headers)

    def test_get_result_object_with_success(self, mock_session, make_mock_response):
        client = TopicExtractionClient(TOKEN)
        url = urljoin(client.base_url, 'jobs/{}/result?'.format(JOB_ID))
        data = {
            'topics': [
                {
                    'topic_name': TOPIC_NAME,
                    'score': SCORE,
                    'informants': [
                        {
                            'content': INFORMANT_CONTENT,
                            'offset': INFORMANT_OFFSET,
                            'length': INFORMANT_LENGTH
                        }
                    ]
                }
            ]
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.get_result_object(JOB_ID)

        assert res == TopicExtractionResult(
            [Topic(
                TOPIC_NAME,
                SCORE,
                [Informant(INFORMANT_CONTENT, offset=INFORMANT_OFFSET, length=INFORMANT_LENGTH)]
            )]
        )
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=client.default_headers)

    def test_get_result_object_with_threshold_with_success(self, mock_session, make_mock_response):
        client = TopicExtractionClient(TOKEN)
        url = urljoin(client.base_url, 'jobs/{0}/result?threshold={1}'.format(JOB_ID, THRESHOLD))
        data = {
            'topics': [
                {
                    'topic_name': TOPIC_NAME,
                    'score': SCORE,
                    'informants': [
                        {
                            'content': INFORMANT_CONTENT,
                            'offset': INFORMANT_OFFSET,
                            'length': INFORMANT_LENGTH
                        }
                    ]
                }
            ]
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.get_result_object(JOB_ID, THRESHOLD)

        assert res == TopicExtractionResult(
            [Topic(
                TOPIC_NAME,
                SCORE,
                [Informant(INFORMANT_CONTENT, offset=INFORMANT_OFFSET, length=INFORMANT_LENGTH)]
            )]
        )
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=client.default_headers)
