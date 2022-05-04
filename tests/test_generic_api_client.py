# -*- coding: utf-8 -*-
"""Unit tests for RevAiApiClient"""

import pytest
import sys

from src.rev_ai.models.customer_url_data import CustomerUrlData
from src.rev_ai.generic_api_client import GenericApiClient
from src.rev_ai import __version__
from tests.helpers import Matcher

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

TOKEN = 'token'
VERSION = 'version'
API = 'api'
JOB_ID = '1'
METADATA = 'test'
NOTIFICATION_URL = 'https://example.com/'
NOTIFICATION_AUTH = 'headers'
CREATED_ON = '2018-05-05T23:23:22.29Z'
LANGUAGE = 'en'

NOTIFICATION_CONFIG = CustomerUrlData(NOTIFICATION_URL, NOTIFICATION_AUTH)


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

        res = client._submit_job({})

        assert res == data
        mock_session.request.assert_called_once_with(
            "POST",
            url,
            json={},
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
        payload = client._enhance_payload({'random': True}, METADATA, None, 0, NOTIFICATION_CONFIG)

        res = client._submit_job(payload)

        assert res == data
        mock_session.request.assert_called_once_with(
            "POST",
            url,
            json=payload,
            headers=client.default_headers)

    def test_get_result_json_with_success(self, mock_session, make_mock_response):
        client = _create_client()
        url = urljoin(client.base_url, 'jobs/{}/result?'.format(JOB_ID))
        data = {
            'random': 'data'
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client._get_result_json(JOB_ID, {})

        assert res == data
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=client.default_headers)

    def test_get_result_json_with_kwargs_with_success(self, mock_session, make_mock_response):
        client = _create_client()
        kwarg_name_1 = 'name1'
        kwarg_value_1 = 1
        kwarg_name_2 = 'name2'
        kwarg_value_2 = 2
        if get_python_major_minor_version() < 35:
            url = urljoin(client.base_url,
                          'jobs/{0}/result?{1}={2}&{3}={4}'.format(JOB_ID,
                                                                   kwarg_name_2,
                                                                   kwarg_value_2,
                                                                   kwarg_name_1,
                                                                   kwarg_value_1))
        else:
            url = urljoin(client.base_url,
                          'jobs/{0}/result?{1}={2}&{3}={4}'.format(JOB_ID,
                                                                   kwarg_name_1,
                                                                   kwarg_value_1,
                                                                   kwarg_name_2,
                                                                   kwarg_value_2))
        data = {
            'random': 'data'
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client._get_result_json(JOB_ID, {kwarg_name_1: kwarg_value_1,
                                               kwarg_name_2: kwarg_value_2,
                                               'invisible': None})

        assert res == data
        mock_session.request.assert_called_once_with(
            "GET",
            Matcher(lambda x: '?name1=1&name2=2' in x or '?name2=2&name1=1' in x),
            headers=client.default_headers)

    def test_get_result_object_with_success(self, mock_session, make_mock_response):
        client = _create_client()
        url = urljoin(client.base_url, 'jobs/{}/result?'.format(JOB_ID))
        data = {
            'random': 'data'
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client._get_result_object(JOB_ID, {})

        assert res == data
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=client.default_headers)

    def test_get_result_object_with_kwargs_with_success(self, mock_session, make_mock_response):
        client = _create_client()
        kwarg_name_1 = 'name1'
        kwarg_value_1 = 1
        kwarg_name_2 = 'name2'
        kwarg_value_2 = 2
        if get_python_major_minor_version() < 35:
            url = urljoin(client.base_url,
                          'jobs/{0}/result?{1}={2}&{3}={4}'.format(JOB_ID,
                                                                   kwarg_name_2,
                                                                   kwarg_value_2,
                                                                   kwarg_name_1,
                                                                   kwarg_value_1))
        else:
            url = urljoin(client.base_url,
                          'jobs/{0}/result?{1}={2}&{3}={4}'.format(JOB_ID,
                                                                   kwarg_name_1,
                                                                   kwarg_value_1,
                                                                   kwarg_name_2,
                                                                   kwarg_value_2))
        data = {
            'random': 'data'
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client._get_result_object(JOB_ID, {kwarg_name_1: kwarg_value_1,
                                                 kwarg_name_2: kwarg_value_2,
                                                 'invisible': None})

        assert res == data
        mock_session.request.assert_called_once_with(
            "GET",
            Matcher(lambda x: '?name1=1&name2=2' in x or '?name2=2&name1=1' in x),
            headers=client.default_headers)


def _create_client():
    return GenericApiClient(TOKEN, API, VERSION, _pass_through_parse, _pass_through_parse)


def _pass_through_parse(x):
    return x


def get_python_major_minor_version():
    return sys.version_info.major * 10 + sys.version_info.minor
