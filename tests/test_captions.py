# -*- coding: utf-8 -*-

import pytest
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai.models import CaptionType

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

JOB_ID = '1'
TOKEN = "token"
URL = urljoin(RevAiAPIClient.base_url, 'jobs/{}/captions'.format(JOB_ID))


@pytest.mark.usefixtures('mock_session', 'make_mock_response')
class TestCaptionEndpoint():
    def test_get_captions_default_content_type(self, mock_session, make_mock_response):
        data = 'Test'
        expected_content_type = CaptionType.SRT.value
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': expected_content_type}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=URL, text=data)
        mock_session.request.return_value = response

        res = client.get_captions(JOB_ID)

        assert res == data
        mock_session.request.assert_called_once_with(
            "GET",
            URL,
            headers=expected_headers
        )

    @pytest.mark.parametrize('content_type', [CaptionType.SRT, CaptionType.VTT])
    def test_get_captions_with_content_type(self, content_type, mock_session, make_mock_response):
        data = 'Test'
        expected_content_type = content_type.value
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': expected_content_type}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=URL, text=data)
        mock_session.request.return_value = response

        res = client.get_captions(JOB_ID, content_type)

        assert res == data
        mock_session.request.assert_called_once_with(
            "GET",
            URL,
            headers=expected_headers
        )

    def test_get_captions_with_speaker_channel(self, mock_session, make_mock_response):
        data = 'Test'
        channel_id = 1
        expected_url = URL + '?speaker_channel={}'.format(channel_id)
        expected_content_type = CaptionType.SRT.value
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': expected_content_type}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=expected_url, text=data)
        mock_session.request.return_value = response

        res = client.get_captions(JOB_ID, channel_id=channel_id)

        assert res == data
        mock_session.request.assert_called_once_with(
            "GET",
            expected_url,
            headers=expected_headers
        )

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_captions_with_no_job_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            RevAiAPIClient(TOKEN).get_captions(id)

    def test_get_captions_as_stream_default_content_type(self, mock_session, make_mock_response):
        data = 'Test'
        expected_content_type = CaptionType.SRT.value
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': expected_content_type}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=URL, text=data)
        mock_session.request.return_value = response

        res = client.get_captions_as_stream(JOB_ID)

        assert res.content == data
        mock_session.request.assert_called_once_with(
            "GET",
            URL,
            headers=expected_headers,
            stream=True
        )

    @pytest.mark.parametrize('content_type', [CaptionType.SRT, CaptionType.VTT])
    def test_get_captions_as_stream_with_content_type(self, content_type,
                                                      mock_session, make_mock_response):
        data = 'Test'
        expected_content_type = content_type.value
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': expected_content_type}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=URL, text=data)
        mock_session.request.return_value = response

        res = client.get_captions_as_stream(JOB_ID, content_type)
        assert res.content == data
        mock_session.request.assert_called_once_with(
            "GET",
            URL,
            headers=expected_headers,
            stream=True
        )

    def test_get_captions_as_stream_with_speaker_channel(self, mock_session, make_mock_response):
        data = 'Test'
        channel_id = 8
        expected_url = URL + '?speaker_channel={}'.format(channel_id)
        expected_content_type = CaptionType.SRT.value
        client = RevAiAPIClient(TOKEN)
        expected_headers = {'Accept': expected_content_type}
        expected_headers.update(client.default_headers)
        response = make_mock_response(url=expected_url, text=data)
        mock_session.request.return_value = response

        res = client.get_captions_as_stream(JOB_ID, channel_id=channel_id)
        assert res.content == data
        mock_session.request.assert_called_once_with(
            "GET",
            expected_url,
            headers=expected_headers,
            stream=True
        )

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_captions_as_stream_with_no_job_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            RevAiAPIClient(TOKEN).get_captions_as_stream(id)
