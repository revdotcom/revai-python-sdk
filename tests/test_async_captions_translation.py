import pytest

from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai.models import RevAiApiDeploymentConfigMap, RevAiApiDeployment

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

TOKEN = "token"
JOB_ID = '1'
SPEECH_TO_TEXT_URL = f"{RevAiApiDeploymentConfigMap[RevAiApiDeployment.US]['base_url']}/speechtotext/v1/"
JOB_ID_URL = urljoin(SPEECH_TO_TEXT_URL, 'jobs/{}'.format(JOB_ID))
JOBS_URL = urljoin(SPEECH_TO_TEXT_URL, 'jobs')


@pytest.mark.usefixtures('mock_session', 'make_mock_response')
class TestAsyncCaptionsTranslation():

    def test_get_translated_captions(self, mock_session, make_mock_response):
        client = RevAiAPIClient(TOKEN)
        url = '{}/captions/translation/{}'.format(JOB_ID_URL, "es")
        response = make_mock_response(url=url, text='es captions')
        mock_session.request.return_value = response

        captions = client.get_translated_captions(JOB_ID, "es")
        assert captions == 'es captions'
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=self.hdr_fixture(client, {'Accept': 'application/x-subrip'}))

    def test_get_translated_captions_as_stream(self, mock_session, make_mock_response):
        client = RevAiAPIClient(TOKEN)
        url = '{}/captions/translation/{}'.format(JOB_ID_URL, "es")
        response = make_mock_response(url=url, text='es captions')
        mock_session.request.return_value = response

        captions = client.get_translated_captions_as_stream(JOB_ID, "es")
        assert captions.content == 'es captions'
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=self.hdr_fixture(client, {'Accept': 'application/x-subrip'}), stream=True)

    @staticmethod
    def hdr_fixture(client: RevAiAPIClient, additional_headers):
        hdr = {}
        hdr.update(client.default_headers)
        hdr.update(additional_headers)
        return hdr
