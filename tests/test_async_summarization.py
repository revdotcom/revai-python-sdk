import json

import pytest

from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai.models import RevAiApiDeploymentConfigMap, RevAiApiDeployment
from src.rev_ai.models.asynchronous.summarization_formatting_options import SummarizationFormattingOptions
from src.rev_ai.models.asynchronous.summarization_job_status import SummarizationJobStatus
from src.rev_ai.models.asynchronous.summarization_options import SummarizationOptions
from src.rev_ai.models.asynchronous.summarization_model import SummarizationModel

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

TOKEN = "token"
JOB_ID = '1'
SPEECH_TO_TEXT_URL = f"{RevAiApiDeploymentConfigMap[RevAiApiDeployment.US]['base_url']}/speechtotext/v1/"
JOB_ID_URL = urljoin(SPEECH_TO_TEXT_URL, 'jobs/{}'.format(JOB_ID))
JOBS_URL = urljoin(SPEECH_TO_TEXT_URL, 'jobs')
JOB_TRANSCRIPT_SUMMARY_URL = '{}/transcript/summary'.format(JOB_ID_URL)


@pytest.mark.usefixtures('mock_session', 'make_mock_response')
class TestAsyncSummarization():

    def test_submit_local_file(self, mocker, mock_session, make_mock_response):
        status = 'transcribed'
        created_on = '2018-05-05T23:23:22.29Z'
        completed_on = '2018-05-05T23:23:22.30Z'
        data = {
            'id': JOB_ID,
            'created_on': created_on,
            'status': status,
            'summarization': {
                'prompt': 'Try to summarize this transcript as good as you possibly can',
                'model': 'premium',
                'type': 'bullets',
                'status': 'completed',
                'completed_on': completed_on
            }
        }
        response = make_mock_response(url=JOB_ID_URL, json_data=data)
        mock_session.request.return_value = response
        client = RevAiAPIClient(TOKEN)

        with mocker.patch('src.rev_ai.apiclient.open', create=True)() as file:
            job = client.submit_job_local_file('test_mp3.mp3',
                                               language="en",
                                               summarization_config=SummarizationOptions(
                                                   prompt="Try to summarize this transcript as good as you possibly can",
                                                   model=SummarizationModel.PREMIUM,
                                                   formatting_type=SummarizationFormattingOptions.BULLETS

                                               ))
        mock_session.request.assert_called_once_with(
            "POST",
            JOBS_URL,
            files={
                'media': ('test_mp3.mp3', file),
                'options': (
                    None,
                    json.dumps({
                        'language': 'en',
                        'summarization_config': {
                            'prompt': "Try to summarize this transcript as good as you possibly can",
                            'model': 'premium',
                            'type': 'bullets'
                        }
                    }, sort_keys=True)
                )
            },
            headers=client.default_headers
        )

        assert job.summarization is not None
        assert job.summarization.model == SummarizationModel.PREMIUM
        assert job.summarization.type == SummarizationFormattingOptions.BULLETS
        assert job.summarization.prompt == "Try to summarize this transcript as good as you possibly can"

    def test_submit_source_url(self, mock_session, make_mock_response):
        status = 'transcribed'
        created_on = '2018-05-05T23:23:22.29Z'
        completed_on = '2018-05-05T23:23:22.30Z'
        data = {
            'id': JOB_ID,
            'status': status,
            'created_on': created_on,
            'summarization': {
                'prompt': 'Try to summarize this transcript as good as you possibly can',
                'model': 'premium',
                'type': 'bullets',
                'status': 'completed',
                'completed_on': completed_on
            }
        }
        response = make_mock_response(url=JOB_ID_URL, json_data=data)
        mock_session.request.return_value = response

        client = RevAiAPIClient(TOKEN)

        job = client.submit_job_url('https://example.com/test.mp3',
                                    language="en",
                                    summarization_config=SummarizationOptions(
                                        "Try to summarize this transcript as good as you possibly can",
                                        SummarizationModel.PREMIUM,
                                        SummarizationFormattingOptions.BULLETS

                                    ))
        mock_session.request.assert_called_once_with(
            "POST",
            JOBS_URL,
            json={
                'media_url': 'https://example.com/test.mp3',
                'language': 'en',
                'summarization_config': {
                    'prompt': "Try to summarize this transcript as good as you possibly can",
                    'model': 'premium',
                    'type': 'bullets'
                }
            },
            headers=client.default_headers
        )

        assert job.summarization is not None
        assert job.summarization.status == SummarizationJobStatus.COMPLETED
        assert job.summarization.model == SummarizationModel.PREMIUM
        assert job.summarization.type == SummarizationFormattingOptions.BULLETS
        assert job.summarization.prompt == "Try to summarize this transcript as good as you possibly can"

    def test_get_transcript_summary_text(self, mock_session, make_mock_response):
        url = JOB_TRANSCRIPT_SUMMARY_URL
        client = RevAiAPIClient(TOKEN)
        response = make_mock_response(url=url, text='transcript summary')
        mock_session.request.return_value = response

        summary = client.get_transcript_summary_text(JOB_ID)
        assert summary == 'transcript summary'
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=self.hdr_fixture(client, {'Accept': 'text/plain'})
        )

    def test_get_transcript_summary_object(self, mock_session, make_mock_response):
        url = JOB_TRANSCRIPT_SUMMARY_URL
        client = RevAiAPIClient(TOKEN)
        data = {
            'summary': 'transcript summary'
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        summary = client.get_transcript_summary_object(JOB_ID)
        assert summary.summary == 'transcript summary'
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=self.hdr_fixture(client, {'Accept': 'application/json'})
        )

    def test_get_transcript_summary_object_paragraph(self, mock_session, make_mock_response):
        url = JOB_TRANSCRIPT_SUMMARY_URL
        data = {
            'summary': 'transcript summary'
        }
        client = RevAiAPIClient(TOKEN)
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        summary = client.get_transcript_summary_object(JOB_ID)
        assert summary.summary == 'transcript summary'
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=self.hdr_fixture(client, {'Accept': 'application/json'})
        )

    def test_get_transcript_summary_json_paragraph_as_stream(self, mock_session, make_mock_response):
        url = JOB_TRANSCRIPT_SUMMARY_URL
        data = {
            "summary": "transcript summary"
        }

        client = RevAiAPIClient(TOKEN)
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        summary = client.get_transcript_summary_json_as_stream(JOB_ID)

        s = summary.content.decode('utf-8')
        s = s.replace('\'', '"')

        assert json.loads(s) == data

        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=self.hdr_fixture(client, {'Accept': 'application/json'}),
            stream=True
        )

    def test_get_transcript_summary_json_bullets(self, mock_session, make_mock_response):
        url = JOB_TRANSCRIPT_SUMMARY_URL
        data = {
            'bullet_points': ['bullet1', 'bullet2']
        }
        client = RevAiAPIClient(TOKEN)
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        summary_json = client.get_transcript_summary_json(JOB_ID)
        assert summary_json is not None
        assert summary_json['bullet_points'] is not None

        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=self.hdr_fixture(client, {'Accept': 'application/json'})
        )

    @staticmethod
    def hdr_fixture(client: RevAiAPIClient, additional_headers):
        hdr = {}
        hdr.update(client.default_headers)
        hdr.update(additional_headers)
        return hdr
