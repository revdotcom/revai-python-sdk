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
URL = urljoin(RevAiAPIClient.base_url, 'jobs/{}/transcript'.format(JOB_ID))


@pytest.mark.usefixtures('mock_client', 'make_mock_response')
class TestTranscriptEndpoints():
    def test_get_transcript_text(self, mock_client, make_mock_response):
        data = 'Test'
        response = make_mock_response(url=URL, text=data)
        mock_client.session.request.return_value = response

        res = mock_client.get_transcript_text(JOB_ID)

        assert res == data
        mock_client.session.request.assert_called_once_with("GET", URL, headers={'Accept': 'text/plain'})

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_transcript_text_with_no_job_id(self, id, mock_client):
        with pytest.raises(ValueError, match='id_ must be provided'):
            mock_client.get_transcript_text(id)

    def test_get_transcript_text_as_stream(self, mock_client, make_mock_response):
        data = 'Test'
        response = make_mock_response(url=URL, text=data)
        mock_client.session.request.return_value = response

        res = mock_client.get_transcript_text_as_stream(JOB_ID)

        assert res.content.decode('utf-8') == data
        mock_client.session.request.assert_called_once_with("GET", URL, headers={'Accept': 'text/plain'}, stream=True)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_transcript_text_as_stream_with_no_job_id(self, id, mock_client):
        with pytest.raises(ValueError, match='id_ must be provided'):
            mock_client.get_transcript_text_as_stream(id)

    def test_get_transcript_json(self, mock_client, make_mock_response):
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
        response = make_mock_response(url=URL, json_data=data)
        mock_client.session.request.return_value = response

        res = mock_client.get_transcript_json(JOB_ID)

        assert res == expected
        mock_client.session.request.assert_called_once_with(
            "GET", URL, headers={'Accept': 'application/vnd.rev.transcript.v1.0+json'})

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_transcript_json_with_no_job_id(self, id, mock_client):
        with pytest.raises(ValueError, match='id_ must be provided'):
            mock_client.get_transcript_json(id)

    def test_get_transcript_json_as_stream(self, mock_client, make_mock_response):
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
        response = make_mock_response(url=URL, json_data=data)
        mock_client.session.request.return_value = response

        res = mock_client.get_transcript_json_as_stream(JOB_ID)

        assert json.loads(res.content.decode('utf-8')) == expected
        mock_client.session.request.assert_called_once_with(
            "GET", URL, headers={'Accept': 'application/vnd.rev.transcript.v1.0+json'}, stream=True)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_transcript_json_as_stream_with_no_job_id(self, id, mock_client):
        with pytest.raises(ValueError, match='id_ must be provided'):
            mock_client.get_transcript_json_as_stream(id)

    def test_get_transcript_object_with_success(self, mock_client, make_mock_response):
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
        response = make_mock_response(url=URL, json_data=data)
        mock_client.session.request.return_value = response

        res = mock_client.get_transcript_object(JOB_ID)

        assert res == expected
        mock_client.session.request.assert_called_once_with(
            "GET", URL, headers={'Accept': 'application/vnd.rev.transcript.v1.0+json'})

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_transcript_object_with_no_job_id(self, id, mock_client):
        with pytest.raises(ValueError, match='id_ must be provided'):
            mock_client.get_transcript_object(id)
