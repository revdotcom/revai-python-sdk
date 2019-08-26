# -*- coding: utf-8 -*-
"""Unit tests for transcript endpoints"""

import pytest
import json
from src.rev_ai.models.asynchronous import Transcript, Monologue, Element
from src.rev_ai.apiclient import RevAiAPIClient

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

JOB_ID = '1'
TOKEN = "token"
URL = urljoin(RevAiAPIClient.base_url, 'jobs/{}/transcript'.format(JOB_ID))


@pytest.mark.usefixtures('mock_session', 'make_mock_response')
class TestTranscriptEndpoints():
    def test_get_transcript_text(self, mock_session, make_mock_response):
        data = 'Test'
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': 'text/plain'}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=URL, text=data)
        mock_session.request.return_value = response

        res = client.get_transcript_text(JOB_ID)

        assert res == data
        mock_session.request.assert_called_once_with("GET",
                                                     URL,
                                                     headers=expected_headers)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_transcript_text_with_no_job_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            RevAiAPIClient(TOKEN).get_transcript_text(id)

    def test_get_transcript_text_as_stream(self, mock_session, make_mock_response):
        data = 'Test'
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': 'text/plain'}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=URL, text=data)
        mock_session.request.return_value = response

        res = client.get_transcript_text_as_stream(JOB_ID)

        assert res.content == data
        mock_session.request.assert_called_once_with("GET",
                                                     URL,
                                                     headers=expected_headers,
                                                     stream=True)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_transcript_text_as_stream_with_no_job_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            RevAiAPIClient(TOKEN).get_transcript_text_as_stream(id)

    def test_get_transcript_json(self, mock_session, make_mock_response):
        data = {
            'monologues': [{
                'speaker': 1,
                'elements': [{
                    'type': 'text',
                    'value': 'Hello',
                    'ts': 0.75,
                    'end_ts': 1.25,
                    'confidence': 0.85
                }]
            }]
        }
        expected = json.loads(json.dumps(data))
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': 'application/vnd.rev.transcript.v1.0+json'}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=URL, json_data=data)
        mock_session.request.return_value = response

        res = client.get_transcript_json(JOB_ID)

        assert res == expected
        mock_session.request.assert_called_once_with(
            "GET", URL, headers=expected_headers)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_transcript_json_with_no_job_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            RevAiAPIClient(TOKEN).get_transcript_json(id)

    def test_get_transcript_json_as_stream(self, mock_session, make_mock_response):
        data = {
            'monologues': [{
                'speaker': 1,
                'elements': [{
                    'type': 'text',
                    'value': 'Hello',
                    'ts': 0.75,
                    'end_ts': 1.25,
                    'confidence': 0.85
                }]
            }]
        }
        expected = json.loads(json.dumps(data))
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': 'application/vnd.rev.transcript.v1.0+json'}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=URL, json_data=data)
        mock_session.request.return_value = response

        res = client.get_transcript_json_as_stream(JOB_ID)

        assert json.loads(res.content.decode('utf-8').replace("\'", "\"")) == expected
        mock_session.request.assert_called_once_with(
            "GET", URL, headers=expected_headers, stream=True)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_transcript_json_as_stream_with_no_job_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            RevAiAPIClient(TOKEN).get_transcript_json_as_stream(id)

    def test_get_transcript_object_with_success(self, mock_session, make_mock_response):
        data = {
            'monologues': [{
                'speaker': 1,
                'elements': [{
                    'type': 'text',
                    'value': 'Hello',
                    'ts': 0.75,
                    'end_ts': 1.25,
                    'confidence': 0.85
                }]
            }]
        }
        expected = Transcript([Monologue(1, [Element('text', 'Hello', 0.75, 1.25, 0.85)])])
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': 'application/vnd.rev.transcript.v1.0+json'}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=URL, json_data=data)
        mock_session.request.return_value = response

        res = client.get_transcript_object(JOB_ID)

        assert res == expected
        mock_session.request.assert_called_once_with(
            "GET", URL, headers=expected_headers)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_transcript_object_with_no_job_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            RevAiAPIClient(TOKEN).get_transcript_object(id)
