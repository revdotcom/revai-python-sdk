# -*- coding: utf-8 -*-
"""Unit tests for job endpoints"""

import json
import pytest
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai.models.asynchronous import Job, JobStatus

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

JOB_ID = '1'
TOKEN = "token"
METADATA = 'test'
CALLBACK_URL = 'https://callback.com/'
CREATED_ON = '2018-05-05T23:23:22.29Z'
MEDIA_URL = 'https://example.com/test.mp3'
FILENAME = 'test.mp3'
JOB_ID_URL = urljoin(RevAiAPIClient.base_url, 'jobs/{}'.format(JOB_ID))
JOBS_URL = urljoin(RevAiAPIClient.base_url, 'jobs')
CUSTOM_VOCAB = [{"phrases": ["word one", "word two"]}]
CUSTOM_VOCAB_ID = "vid"
LANGUAGE = 'en'


@pytest.mark.usefixtures('mock_session', 'make_mock_response')
class TestJobEndpoints():
    def test_get_job_details_with_success(self, mock_session, make_mock_response):
        status = 'transcribed'
        created_on = '2018-05-05T23:23:22.29Z'
        data = {
            'id': JOB_ID,
            'status': status,
            'created_on': created_on
        }
        response = make_mock_response(url=JOB_ID_URL, json_data=data)
        mock_session.request.return_value = response
        client = RevAiAPIClient(TOKEN)

        res = client.get_job_details(JOB_ID)

        assert res == Job(JOB_ID, created_on, JobStatus.TRANSCRIBED)
        mock_session.request.assert_called_once_with("GET",
                                                     JOB_ID_URL,
                                                     headers=client.default_headers)

    @pytest.mark.parametrize('id', [None, ''])
    def test_get_job_details_with_no_job_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            RevAiAPIClient(TOKEN).get_job_details(id)

    def test_get_list_of_jobs_limit_with_success(self, mock_session, make_mock_response):
        status = 'transcribed'
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
        url = JOBS_URL + "?limit=2"
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response
        client = RevAiAPIClient(TOKEN)

        res = client.get_list_of_jobs(limit=2)

        assert isinstance(res, list)
        assert len(res) == 2
        mock_session.request.assert_called_once_with("GET", url, headers=client.default_headers)

    def test_get_list_of_jobs_starting_after_with_success(self, mock_session, make_mock_response):
        status = 'transcribed'
        created_on = '2018-05-05T23:23:22.29Z'
        data = [
            {
                'id': JOB_ID,
                'status': status,
                'created_on': created_on
            }
        ]
        url = JOBS_URL + "?starting_after=4"
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response
        client = RevAiAPIClient(TOKEN)

        res = client.get_list_of_jobs(starting_after="4")

        assert isinstance(res, list)
        assert len(res) == 1
        mock_session.request.assert_called_once_with("GET", url, headers=client.default_headers)

    def test_submit_job_url_with_success(self, mock_session, make_mock_response):
        data = {
            'id': JOB_ID,
            'status': 'in_progress',
            'created_on': CREATED_ON,
            'metadata': METADATA,
            'callback_url': CALLBACK_URL,
            'skip_diarization': True,
            'skip_punctuation': True,
            'speaker_channels_count': 1,
            'filter_profanity': True,
            'remove_disfluencies': True,
            'delete_after_seconds': 0,
            'language': LANGUAGE
        }
        response = make_mock_response(url=JOB_ID_URL, json_data=data)
        mock_session.request.return_value = response
        client = RevAiAPIClient(TOKEN)

        res = client.submit_job_url(MEDIA_URL, METADATA,
                                    CALLBACK_URL, True,
                                    True, 1, CUSTOM_VOCAB, True,
                                    True, 0, LANGUAGE, CUSTOM_VOCAB_ID)

        assert res == Job(JOB_ID,
                          CREATED_ON,
                          JobStatus.IN_PROGRESS,
                          metadata=METADATA,
                          callback_url=CALLBACK_URL)
        mock_session.request.assert_called_once_with(
            "POST",
            JOBS_URL,
            json={
                'media_url': MEDIA_URL,
                'callback_url': CALLBACK_URL,
                'metadata': METADATA,
                'skip_diarization': True,
                'skip_punctuation': True,
                'speaker_channels_count': 1,
                'custom_vocabularies': CUSTOM_VOCAB,
                'filter_profanity': True,
                'remove_disfluencies': True,
                'delete_after_seconds': 0,
                'language': LANGUAGE,
                'custom_vocabulary_id': CUSTOM_VOCAB_ID
            },
            headers=client.default_headers)

    @pytest.mark.parametrize('url', [None, ''])
    def test_submit_job_url_with_no_media_url(self, url, mock_session):
        with pytest.raises(ValueError, match='media_url must be provided'):
            RevAiAPIClient(TOKEN).submit_job_url(url)

    def test_submit_job_local_file_with_success(self, mocker, mock_session, make_mock_response):
        created_on = '2018-05-05T23:23:22.29Z'
        data = {
            'id': JOB_ID,
            'status': 'in_progress',
            'created_on': created_on,
            'metadata': METADATA,
            'callback_url': CALLBACK_URL,
            'skip_punctuation': True,
            'skip_diarization': True,
            'speaker_channels_count': 1,
            'filter_profanity': True,
            'remove_disfluencies': True,
            'delete_after_seconds': 0,
            'language': LANGUAGE
        }
        response = make_mock_response(url=JOB_ID_URL, json_data=data)
        mock_session.request.return_value = response
        client = RevAiAPIClient(TOKEN)

        with mocker.patch('src.rev_ai.apiclient.open', create=True)() as file:
            res = client.submit_job_local_file(FILENAME, METADATA,
                                               CALLBACK_URL, True,
                                               True, 1, CUSTOM_VOCAB, True,
                                               True, 0, LANGUAGE, CUSTOM_VOCAB_ID)

            assert res == Job(JOB_ID,
                              CREATED_ON,
                              JobStatus.IN_PROGRESS,
                              metadata=METADATA,
                              callback_url=CALLBACK_URL)
            mock_session.request.assert_called_once_with(
                "POST",
                JOBS_URL,
                files={
                    'media': (FILENAME, file),
                    'options': (
                        None,
                        json.dumps({
                            'metadata': METADATA,
                            'callback_url': CALLBACK_URL,
                            'skip_punctuation': True,
                            'skip_diarization': True,
                            'speaker_channels_count': 1,
                            'custom_vocabularies': CUSTOM_VOCAB,
                            'filter_profanity': True,
                            'remove_disfluencies': True,
                            'delete_after_seconds': 0,
                            'language': LANGUAGE,
                            'custom_vocabulary_id': CUSTOM_VOCAB_ID
                        }, sort_keys=True)
                    )
                },
                headers=client.default_headers)

    @pytest.mark.parametrize('filename', [None, ''])
    def test_submit_job_url_with_no_filename(self, filename, mock_session):
        with pytest.raises(ValueError, match='filename must be provided'):
            RevAiAPIClient(TOKEN).submit_job_local_file(filename, None)

    def test_delete_job_success(self, mock_session, make_mock_response):
        response = make_mock_response(url=JOB_ID_URL, status=204)
        mock_session.request.return_value = response
        client = RevAiAPIClient(TOKEN)

        res = client.delete_job(JOB_ID)

        assert res is None
        mock_session.request.assert_called_once_with("DELETE",
                                                     JOB_ID_URL,
                                                     headers=client.default_headers)

    @pytest.mark.parametrize('id', [None, ''])
    def test_delete_job_with_no_id(self, id, mock_session):
        with pytest.raises(ValueError, match='id_ must be provided'):
            RevAiAPIClient(TOKEN).delete_job(id)
