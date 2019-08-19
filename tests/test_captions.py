# -*- coding: utf-8 -*-

import pytest
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai.models import CaptionType

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

JOB_ID = '1'
URL = urljoin(RevAiAPIClient.base_url, 'jobs/{}/captions'.format(JOB_ID))


@pytest.mark.usefixtures('mock_client', 'make_mock_response')
class TestCaptionEndpoint():
    def test_get_captions(self, mock_client, make_mock_response):
        data = 'Test'
        if sys.version_info > (3, 0):
            expected_content_type = CaptionType.SRT.value
        else:
            expected_content_type = CaptionType.SRT
        response = make_mock_response(url=URL, text=data)
        mock_client.session.request.return_value = response

        res = mock_client.get_captions(JOB_ID)

        assert res == data
        mock_client.session.request.assert_called_once_with(
            "GET",
            URL,
            headers={'Accept': 'application/x-subrip'}
        )

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_captions_with_no_job_id(self, id, mock_client):
        with pytest.raises(ValueError, match='id_ must be provided'):
            mock_client.get_captions(id)

    def test_get_captions_as_stream(self, mock_client, make_mock_response):
        data = 'Test'
        if sys.version_info > (3, 0):
            expected_content_type = CaptionType.SRT.value
        else:
            expected_content_type = CaptionType.SRT
        response = make_mock_response(url=URL, text=data)
        mock_client.session.request.return_value = response

        res = mock_client.get_captions_as_stream(JOB_ID)

        assert res.content.decode('utf-8') == data
        mock_client.session.request.assert_called_once_with(
            "GET",
            URL,
            headers={'Accept': 'application/x-subrip'},
            stream=True
        )

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_captions_as_stream_with_no_job_id(self, id, mock_client):
        with pytest.raises(ValueError, match='id_ must be provided'):
            mock_client.get_captions_as_stream(id)
