import json

import pytest

from src.rev_ai import JobStatus
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai.models.asynchronous.summarization_formatting_options import SummarizationFormattingOptions
from src.rev_ai.models.asynchronous.summarization_job_status import SummarizationJobStatus
from src.rev_ai.models.asynchronous.summarization_options import SummarizationOptions
from src.rev_ai.models.asynchronous.translation_job_status import TranslationJobStatus
from src.rev_ai.models.asynchronous.translation_language_options import TranslationLanguageOptions
from src.rev_ai.models.asynchronous.translation_options import TranslationOptions
from src.rev_ai.models.nlp_model import NlpModel

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

TOKEN = "token"
JOB_ID = '1'
JOB_ID_URL = urljoin(RevAiAPIClient.base_url, 'jobs/{}'.format(JOB_ID))
JOBS_URL = urljoin(RevAiAPIClient.base_url, 'jobs')


@pytest.mark.usefixtures('mock_session', 'make_mock_response')
class TestSuperApi():

    def test_super_api_local_file(self, mocker, mock_session, make_mock_response):
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
            },
            'translation': {
                'target_languages': [
                    {
                        'language': 'es',
                        'model': 'premium',
                        'status': 'completed'
                    },
                    {
                        'language': 'ru',
                        'model': 'premium',
                        'status': 'completed'
                    }
                ],
                'completed_on': completed_on
            }
        }
        response = make_mock_response(url=JOB_ID_URL, json_data=data)
        mock_session.request.return_value = response
        client = RevAiAPIClient(TOKEN)

        with mocker.patch('src.rev_ai.apiclient.open', create=True)() as file:
            job = client.submit_job_local_file('test_mp3.mp3',
                                           metadata="python sdk SuperApi test",
                                           delete_after_seconds=50000,
                                           language="en",
                                           summarization_config=SummarizationOptions(
                                               "Try to summarize this transcript as good as you possibly can",
                                               NlpModel.PREMIUM,
                                               SummarizationFormattingOptions.BULLETS

                                           ),
                                           translation_config=TranslationOptions(
                                               target_languages=[
                                                   TranslationLanguageOptions("es", NlpModel.PREMIUM),
                                                   TranslationLanguageOptions("ru")
                                               ]
                                           )
                                           )
        mock_session.request.assert_called_once_with(
            "POST",
            JOBS_URL,
            files={
                'media': ('test_mp3.mp3', file),
                'options': (
                    None,
                    json.dumps({
                        'metadata': "python sdk SuperApi test",
                        'delete_after_seconds': 50000,
                        'language':'en',
                        'summarization_config':{
                            'prompt': "Try to summarize this transcript as good as you possibly can",
                            'model':'premium',
                            'type':'bullets'
                        },
                        'translation_config':{
                            'target_languages':[
                            {
                                'language':'es',
                                'model':'premium'
                            },
                            {
                                'language':'ru'
                            }

                        ]}
                    }, sort_keys=True)
                )
            },
            headers=client.default_headers
        )
        self.assert_job(client, job, mock_session, make_mock_response)

    def test_super_api_source_url(self, mock_session, make_mock_response):
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
            },
            'translation': {
                'target_languages': [
                    {
                        'language': 'es',
                        'model': 'premium',
                        'status': 'completed'
                    },
                    {
                        'language': 'ru',
                        'model': 'premium',
                        'status': 'completed'
                    }
                ],
                'completed_on': completed_on
            }
        }
        response = make_mock_response(url=JOB_ID_URL, json_data=data)
        mock_session.request.return_value = response

        client = RevAiAPIClient(TOKEN)

        job = client.submit_job_url('https://example.com/test.mp3',
                                    metadata="python sdk SuperApi test",
                                    delete_after_seconds=50000,
                                    language="en",
                                    summarization_config=SummarizationOptions(
                                        "Try to summarize this transcript as good as you possibly can",
                                        NlpModel.PREMIUM,
                                        SummarizationFormattingOptions.BULLETS

                                    ),
                                    translation_config=TranslationOptions(
                                        target_languages=[
                                            TranslationLanguageOptions("es", NlpModel.PREMIUM),
                                            TranslationLanguageOptions("ru")
                                        ]
                                    )
                                    )
        mock_session.request.assert_called_once_with(
            "POST",
            JOBS_URL,
            json={
                        'metadata': "python sdk SuperApi test",
                        'media_url':'https://example.com/test.mp3',
                        'delete_after_seconds': 50000,
                        'language': 'en',
                        'summarization_config': {
                            'prompt': "Try to summarize this transcript as good as you possibly can",
                            'model': 'premium',
                            'type': 'bullets'
                        },
                        'translation_config': {
                            'target_languages': [
                                {
                                    'language': 'es',
                                    'model': 'premium'
                                },
                                {
                                    'language': 'ru'
                                }

                            ]}
            },
            headers=client.default_headers
        )
        self.assert_job(client, job, mock_session, make_mock_response)
    def assert_job(self, client, job, mock_session, make_mock_response):
        assert job.summarization is not None
        assert job.summarization.model == NlpModel.PREMIUM
        assert job.summarization.type == SummarizationFormattingOptions.BULLETS
        assert job.summarization.prompt == "Try to summarize this transcript as good as you possibly can"

        assert job.translation is not None
        assert job.translation.target_languages is not None
        assert len(job.translation.target_languages) == 2

        assert job.status.name == JobStatus.TRANSCRIBED.name
        assert job.summarization.status == SummarizationJobStatus.COMPLETED

        assert job.translation.completed_on is not None
        assert job.translation.target_languages[0].status == TranslationJobStatus.COMPLETED
        assert job.translation.target_languages[0].language == "es"
        assert job.translation.target_languages[0].model == NlpModel.PREMIUM

        assert job.translation.target_languages[1].status, TranslationJobStatus.COMPLETED
        assert job.translation.target_languages[1].language, "ru"

        mock_session.reset_mock()
        url = '{}/transcript/summary'.format(JOB_ID_URL)
        hdr = {}
        hdr.update(client.default_headers)
        hdr.update({'Accept': 'text/plain'})
        response = make_mock_response(url=url, text='transcript summary')
        mock_session.request.return_value = response

        summary = client.get_transcript_summary_text(job.id)
        assert summary == 'transcript summary'
        mock_session.request.assert_called_once_with("GET", url, headers=hdr)

        mock_session.reset_mock()
        data = {
            'bullet_points': ['bullet1', 'bullet2']
        }
        url = '{}/transcript/summary'.format(JOB_ID_URL)
        hdr = {}
        hdr.update(client.default_headers)
        hdr.update({'Accept': 'application/json'})
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        summary_json = client.get_transcript_summary_json(job.id)
        assert summary_json is not None
        assert summary_json.bullet_points is not None
        assert len(summary_json.bullet_points) > 0
        mock_session.request.assert_called_once_with("GET", url, headers=hdr)

        mock_session.reset_mock()
        data = {
            'bullet_points': ['bullet1', 'bullet2']
        }
        url = '{}/transcript/summary'.format(JOB_ID_URL)
        hdr = {}
        hdr.update(client.default_headers)
        hdr.update({'Accept': 'application/json'})
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        summary_json_stream = client.get_transcript_summary_json_as_stream(job.id)
        assert summary_json_stream is not None
        mock_session.request.assert_called_once_with("GET", url, headers=hdr, stream=True)

        mock_session.reset_mock()
        url = '{}/transcript/translation/{}'.format(JOB_ID_URL, "es")
        hdr = {}
        hdr.update(client.default_headers)
        hdr.update({'Accept': 'text/plain'})
        response = make_mock_response(url=url, text='es transcript')
        mock_session.request.return_value = response

        translation1 = client.get_translated_transcript_text(job.id, "es")
        assert translation1 is not None
        mock_session.request.assert_called_once_with("GET", url, headers=hdr)

        mock_session.reset_mock()
        data = {
            'monologues': []
        }
        url = '{}/transcript/translation/{}'.format(JOB_ID_URL, 'es')
        hdr = {}
        hdr.update(client.default_headers)
        hdr.update({'Accept': 'application/vnd.rev.transcript.v1.0+json'})
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        translation1_json = client.get_translated_transcript_json(job.id, "es")
        assert translation1_json is not None
        mock_session.request.assert_called_once_with("GET", url, headers=hdr)

        mock_session.reset_mock()
        data = {
            'monologues': []
        }
        url = '{}/transcript/translation/{}'.format(JOB_ID_URL, 'es')
        hdr = {}
        hdr.update(client.default_headers)
        hdr.update({'Accept': 'application/vnd.rev.transcript.v1.0+json'})
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        translation1_json_stream = client.get_translated_transcript_json_as_stream(job.id, "es")
        assert translation1_json_stream is not None
        mock_session.request.assert_called_once_with("GET", url, headers=hdr, stream=True)

        mock_session.reset_mock()
        data = {
            'monologues': [
                {'speaker': 123}
            ]
        }
        url = '{}/transcript/translation/{}'.format(JOB_ID_URL, 'es')
        hdr = {}
        hdr.update(client.default_headers)
        hdr.update({'Accept': 'application/vnd.rev.transcript.v1.0+json'})
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        translation1_object = client.get_translated_transcript_object(job.id, "es")
        assert translation1_object is not None
        assert translation1_object.monologues[0].speaker == 123
        mock_session.request.assert_called_once_with("GET", url, headers=hdr)
