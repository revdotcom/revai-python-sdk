# -*- coding: utf-8 -*-
"""Unit tests for RevAiApiClient"""

import pytest
from src.rev_ai.generic_api_client import GenericApiClient
from src.rev_ai import __version__
from src.rev_ai import JobStatus

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

TOKEN = 'token'
VERSION = 'version'
API = 'api'
JOB_ID = '1'
METADATA = 'test'
CALLBACK_URL = 'https://example.com/'
CREATED_ON = '2018-05-05T23:23:22.29Z'
LANGUAGE = 'en'


class TestGenericApiClient:
    def test_constructor_with_success(self):
        client = _create_client()

        headers = client.default_headers

        assert headers.get('User-Agent') == 'RevAi-PythonSDK/{}'.format(__version__)
        assert headers.get('Authorization') == 'Bearer {}'.format(TOKEN)
        assert client.base_url == 'https://api.rev.ai/{0}/{1}/'.format(API, VERSION)

    @pytest.mark.parametrize('token', [None, ''])
    def test_constructor_with_no_token(self, token):
        with pytest.raises(ValueError, match='access_token must be provided'):
            GenericApiClient(token, "v1", "api", lambda x: x, lambda x: x)

    def test_delete_job_success(self, mock_session, make_mock_response):
        client = _create_client()
        url = urljoin(client.base_url, 'jobs/{}'.format(JOB_ID))
        response = make_mock_response(url=url, status=204)
        mock_session.request.return_value = response

        res = client.delete_job(JOB_ID)

        assert res is None
        mock_session.request.assert_called_once_with("DELETE",
                                                     url,
                                                     headers=client.default_headers)

    @pytest.mark.parametrize('id', [None, ''])
    def test_delete_job_with_no_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            _create_client().delete_job(id)

    @pytest.mark.usefixtures('mock_session', 'make_mock_response')
    def test_get_job_details_with_success(self, mock_session, make_mock_response):
        client = _create_client()
        url = urljoin(client.base_url, 'jobs/{}'.format(JOB_ID))
        status = 'completed'
        created_on = '2018-05-05T23:23:22.29Z'
        data = {
            'id': JOB_ID,
            'status': status,
            'created_on': created_on
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.get_job_details(JOB_ID)

        assert res == data
        mock_session.request.assert_called_once_with("GET",
                                                     url,
                                                     headers=client.default_headers)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_job_details_with_no_job_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            _create_client().get_job_details(id)

    def test_get_list_of_jobs_limit_with_success(self, mock_session, make_mock_response):
        client = _create_client()
        url = urljoin(client.base_url, 'jobs?limit=2')
        status = 'completed'
        created_on = '2018-05-05T23:23:22.29Z'
        data = [
            {
                'id': JOB_ID,
                'status': status,
                'created_on': created_on
            },
            {
                'id': '2',
                'status': 'in_progress',
                'created_on': created_on
            }
        ]
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.get_list_of_jobs(limit=2)

        assert isinstance(res, list)
        assert len(res) == 2
        mock_session.request.assert_called_once_with("GET", url, headers=client.default_headers)

    def test_get_list_of_jobs_starting_after_with_success(self, mock_session, make_mock_response):
        client = _create_client()
        url = urljoin(client.base_url, 'jobs?starting_after=4')
        status = 'completed'
        created_on = '2018-05-05T23:23:22.29Z'
        data = [
            {
                'id': JOB_ID,
                'status': status,
                'created_on': created_on
            }
        ]
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.get_list_of_jobs(starting_after="4")

        assert isinstance(res, list)
        assert len(res) == 1
        mock_session.request.assert_called_once_with("GET", url, headers=client.default_headers)

    def test_submit_job_empty_payload_with_success(self, mock_session, make_mock_response):
        client = _create_client()
        url = urljoin(client.base_url, 'jobs')
        data = {
            'id': JOB_ID,
            'status': 'in_progress',
            'delete_after_seconds': 0
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client._submit_job(payload={},
                                 metadata=METADATA,
                                 callback_url=CALLBACK_URL,
                                 delete_after_seconds=0,
                                 language=LANGUAGE)

        assert res == data
        mock_session.request.assert_called_once_with(
            "POST",
            url,
            json={
                'callback_url': CALLBACK_URL,
                'metadata': METADATA,
                'delete_after_seconds': 0,
                'language': LANGUAGE
            },
            headers=client.default_headers)

    def test_submit_job_nonempty_payload_with_success(self, mock_session, make_mock_response):
        client = _create_client()
        url = urljoin(client.base_url, 'jobs')
        data = {
            'id': JOB_ID,
            'status': 'in_progress',
            'delete_after_seconds': 0
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client._submit_job(payload={'random': True},
                                 metadata=METADATA,
                                 callback_url=CALLBACK_URL,
                                 delete_after_seconds=0,
                                 language=LANGUAGE)

        assert res == data
        mock_session.request.assert_called_once_with(
            "POST",
            url,
            json={
                'random': True,
                'callback_url': CALLBACK_URL,
                'metadata': METADATA,
                'delete_after_seconds': 0,
                'language': LANGUAGE
            },
            headers=client.default_headers)


def _create_client():
    return GenericApiClient(TOKEN, API, VERSION, _pass_through_parse, _pass_through_parse)


def _pass_through_parse(x):
    return x
