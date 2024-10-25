import json

import pytest

from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai.models import RevAiApiDeploymentConfigMap, RevAiApiDeployment
from src.rev_ai.models.asynchronous.translation_job_status import TranslationJobStatus
from src.rev_ai.models.asynchronous.translation_language_options import TranslationLanguageOptions
from src.rev_ai.models.asynchronous.translation_options import TranslationOptions
from src.rev_ai.models.asynchronous.translation_model import TranslationModel

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
class TestAsyncTranslation():

    def test_submit_local_file(self, mocker, mock_session, make_mock_response):
        created_on = '2018-05-05T23:23:22.30Z'
        completed_on = '2018-05-05T23:24:22.30Z'
        status = 'transcribed'
        data = {
            'id': JOB_ID,
            'created_on': created_on,
            'status': status,
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
                                               language="en",
                                               translation_config=TranslationOptions(
                                                   target_languages=[
                                                       TranslationLanguageOptions("es", TranslationModel.PREMIUM),
                                                       TranslationLanguageOptions("ru")
                                                   ]
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
                    }, sort_keys=True)
                )
            },
            headers=client.default_headers
        )
        assert job.translation is not None
        assert job.translation.target_languages is not None
        assert len(job.translation.target_languages) == 2

        assert job.translation.completed_on is not None
        assert job.translation.target_languages[0].status == TranslationJobStatus.COMPLETED
        assert job.translation.target_languages[0].language == "es"
        assert job.translation.target_languages[0].model == TranslationModel.PREMIUM

        assert job.translation.target_languages[1].status, TranslationJobStatus.COMPLETED
        assert job.translation.target_languages[1].language, "ru"

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
                                    language="en",
                                    translation_config=TranslationOptions(
                                        target_languages=[
                                            TranslationLanguageOptions("es", TranslationModel.PREMIUM),
                                            TranslationLanguageOptions("ru")
                                        ]
                                    )
                                    )
        mock_session.request.assert_called_once_with(
            "POST",
            JOBS_URL,
            json={
                'media_url': 'https://example.com/test.mp3',
                'language': 'en',
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
        assert job.translation is not None
        assert job.translation.target_languages is not None
        assert len(job.translation.target_languages) == 2

        assert job.translation.completed_on is not None
        assert job.translation.target_languages[0].status == TranslationJobStatus.COMPLETED
        assert job.translation.target_languages[0].language == "es"
        assert job.translation.target_languages[0].model == TranslationModel.PREMIUM

        assert job.translation.target_languages[1].status, TranslationJobStatus.COMPLETED
        assert job.translation.target_languages[1].language, "ru"

    def test_get_translated_transcript_text(self, mock_session, make_mock_response):
        client = RevAiAPIClient(TOKEN)
        url = '{}/transcript/translation/{}'.format(JOB_ID_URL, "es")
        response = make_mock_response(url=url, text='es transcript')
        mock_session.request.return_value = response

        translation = client.get_translated_transcript_text(JOB_ID, "es")
        assert translation == 'es transcript'
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=self.hdr_fixture(client, {'Accept': 'text/plain'}))

    def test_get_translated_transcript_json(self, mock_session, make_mock_response):
        client = RevAiAPIClient(TOKEN)
        url = '{}/transcript/translation/{}'.format(JOB_ID_URL, "es")
        data = {
            'monologues': []
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        translation = client.get_translated_transcript_json(JOB_ID, "es")
        assert translation == data
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=self.hdr_fixture(client, {'Accept': 'application/vnd.rev.transcript.v1.0+json'}))

    def test_get_translated_transcript_json_as_stream(self, mock_session, make_mock_response):
        client = RevAiAPIClient(TOKEN)
        url = '{}/transcript/translation/{}'.format(JOB_ID_URL, "es")
        data = {
            'monologues': []
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        translation = client.get_translated_transcript_json_as_stream(JOB_ID, "es")
        s = translation.content.decode('utf-8')
        s = s.replace('\'', '"')
        assert json.loads(s) == data
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=self.hdr_fixture(client, {'Accept': 'application/vnd.rev.transcript.v1.0+json'}), stream=True)

    def test_get_translated_transcript_object(self, mock_session, make_mock_response):
        client = RevAiAPIClient(TOKEN)
        url = '{}/transcript/translation/{}'.format(JOB_ID_URL, "es")
        data = {
            'monologues': [
                {'speaker': 123}
            ]
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        translation = client.get_translated_transcript_object(JOB_ID, "es")
        assert translation.monologues[0].speaker == 123
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=self.hdr_fixture(client, {'Accept': 'application/vnd.rev.transcript.v1.0+json'}))

    @staticmethod
    def hdr_fixture(client: RevAiAPIClient, additional_headers):
        hdr = {}
        hdr.update(client.default_headers)
        hdr.update(additional_headers)
        return hdr
