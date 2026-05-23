# -*- coding: utf-8 -*-
"""Unit tests for Forced Alignment Client"""

import json
import pytest
from src.rev_ai.forced_alignment_client import ForcedAlignmentClient
from src.rev_ai import __version__
from src.rev_ai.models.forced_alignment import ForcedAlignmentJob, ForcedAlignmentResult, Monologue, ElementAlignment
from src.rev_ai.models import JobStatus, CustomerUrlData

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

TOKEN = 'token'
JOB_ID = '1'
METADATA = 'test'
MEDIA_URL = 'https://www.rev.ai/FTC_Sample_1.mp3'
TRANSCRIPT_URL = 'https://www.rev.ai/FTC_Sample_1.txt'
TRANSCRIPT_TEXT = """Hi, my name is Jack Groetzinger and I'm going to be talking about how to recruit a cofounder and a team for your startup. I'm going to first give a quick overview of what we're going to talk about. We're going to start out by talking about the sorts of folks you might be looking for for your startup. Then we'll dive right into tactics and approaches you can use to get inbound interest in your company. We'll talk a little bit about how to get people excited for your startup, and then we'll talk about the screening process, how to figure out if someone is a good match and someone you should make an offer to. We'll then cover how you make an offer and we'll wrap up by covering a few specific issues, one is technical hiring, which can be a little different from more general recruiting and finally we'll talk about specifically what you should do when you're looking for a cofounder. Many of the things we're going to be talking about are applicable to both finding a cofounder and finding employees, but there are a few specific issues that are relevant to when you're looking for a co-founder to be part of your startup, so we'll talk about that I want to give a quick background in myself, I am the cofounder of SeatGeek. We are a search engine for sports and concert tickets based in New York City, this is my third startup and for all three we built a team so I have some experience with this. At SeetGeek we have 17 folks and we have an incredible team. And I just want to talk about some things that we've done that I think have helped us get there as sort of the overall thesis for this, one thing that's worth keeping in mind is that recruiting is a lot of work. Some people think that you can raise money and spend a few weeks building your team and then move on to more interesting things, that's totally not the case, recruiting is something that you're always doing, I as a co-founder probably spend regularly 30% of my time trying to find new people to add to our team. But if you, you it's a lot of work because it's such an important thing to assess the success of a startup, and if you invest that time, then the dividends pay off."""
CREATED_ON = '2025-01-11T22:42:23.45Z'
LANGUAGE = 'en'


class TestForcedAlignmentClient:
    def test_constructor_with_success(self):
        client = ForcedAlignmentClient(TOKEN)

        headers = client.default_headers

        assert headers.get('User-Agent') == 'RevAi-PythonSDK/{}'.format(__version__)
        assert headers.get('Authorization') == 'Bearer {}'.format(TOKEN)
        assert client.base_url == 'https://api.rev.ai/alignment/v1/'

    @pytest.mark.parametrize('token', [None, ''])
    def test_constructor_with_no_token(self, token):
        with pytest.raises(ValueError, match='access_token must be provided'):
            ForcedAlignmentClient(token)

    def test_submit_job_url_with_source_config_success(self, mock_session, make_mock_response):
        client = ForcedAlignmentClient(TOKEN)
        url = urljoin(client.base_url, 'jobs')
        source_config = CustomerUrlData(MEDIA_URL)
        transcript_text = TRANSCRIPT_TEXT
        data = {
            'id': JOB_ID,
            'created_on': CREATED_ON,
            'status': 'in_progress',
            'metadata': METADATA,
            'type': 'alignment',
            'language': LANGUAGE
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.submit_job_url(
            source_config=source_config,
            transcript_text=transcript_text,
            metadata=METADATA,
            language=LANGUAGE)

        assert res == ForcedAlignmentJob(
            id=JOB_ID,
            created_on=CREATED_ON,
            status=JobStatus.IN_PROGRESS,
            metadata=METADATA,
            type='alignment')

        mock_session.request.assert_called_once_with(
            "POST",
            url,
            json={
                'source_config': source_config.to_dict(),
                'transcript_text': transcript_text,
                'metadata': METADATA,
                'language': LANGUAGE
            },
            headers=client.default_headers)

    def test_submit_job_url_with_transcript_config_success(self, mock_session, make_mock_response):
        client = ForcedAlignmentClient(TOKEN)
        url = urljoin(client.base_url, 'jobs')
        source_config = CustomerUrlData(MEDIA_URL)
        source_transcript_config = CustomerUrlData(TRANSCRIPT_URL)
        data = {
            'id': JOB_ID,
            'created_on': CREATED_ON,
            'status': 'in_progress',
            'metadata': METADATA,
            'type': 'alignment'
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.submit_job_url(
            source_config=source_config,
            source_transcript_config=source_transcript_config,
            metadata=METADATA)

        assert res == ForcedAlignmentJob(
            id=JOB_ID,
            created_on=CREATED_ON,
            status=JobStatus.IN_PROGRESS,
            metadata=METADATA,
            type='alignment')

        mock_session.request.assert_called_once_with(
            "POST",
            url,
            json={
                'source_config': source_config.to_dict(),
                'source_transcript_config': source_transcript_config.to_dict(),
                'metadata': METADATA
            },
            headers=client.default_headers)

    def test_submit_job_url_missing_source_config(self):
        client = ForcedAlignmentClient(TOKEN)
        with pytest.raises(ValueError, match='source_config must be provided'):
            client.submit_job_url(transcript_text=TRANSCRIPT_TEXT)

    def test_submit_job_url_missing_transcript(self):
        client = ForcedAlignmentClient(TOKEN)
        source_config = CustomerUrlData(MEDIA_URL)
        with pytest.raises(ValueError, match='Either source_transcript_config or transcript_text must be provided'):
            client.submit_job_url(source_config=source_config)

    def test_submit_job_url_both_transcript_options(self):
        client = ForcedAlignmentClient(TOKEN)
        source_config = CustomerUrlData(MEDIA_URL)
        source_transcript_config = CustomerUrlData(TRANSCRIPT_URL)
        with pytest.raises(ValueError, match='Only one of source_transcript_config or transcript_text may be provided'):
            client.submit_job_url(
                source_config=source_config,
                source_transcript_config=source_transcript_config,
                transcript_text=TRANSCRIPT_TEXT)

    def test_get_result_json_with_success(self, mock_session, make_mock_response):
        client = ForcedAlignmentClient(TOKEN)
        url = urljoin(client.base_url, 'jobs/{}/transcript'.format(JOB_ID))
        data = {
            'monologues': [
                {
                    'speaker': 0,
                    'elements': [
                        {
                            'type': 'text',
                            'value': 'Hi',
                            'ts': 0.25,
                            'end_ts': 0.5
                        },
                        {
                            'type': 'text',
                            'value': 'my',
                            'ts': 0.6,
                            'end_ts': 0.75
                        },
                        {
                            'type': 'text',
                            'value': 'name',
                            'ts': 0.8,
                            'end_ts': 1.1
                        },
                        {
                            'type': 'text',
                            'value': 'is',
                            'ts': 1.2,
                            'end_ts': 1.3
                        },
                        {
                            'type': 'text',
                            'value': 'Jack',
                            'ts': 1.4,
                            'end_ts': 1.7
                        }
                    ]
                }
            ]
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.get_result_json(JOB_ID)

        assert res == data
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=client.default_headers)

    def test_get_result_object_with_success(self, mock_session, make_mock_response):
        client = ForcedAlignmentClient(TOKEN)
        url = urljoin(client.base_url, 'jobs/{}/transcript'.format(JOB_ID))
        data = {
            'monologues': [
                {
                    'speaker': 0,
                    'elements': [
                        {
                            'type': 'text',
                            'value': 'Hi',
                            'ts': 0.25,
                            'end_ts': 0.5
                        },
                        {
                            'type': 'text',
                            'value': 'my',
                            'ts': 0.6,
                            'end_ts': 0.75
                        },
                        {
                            'type': 'text',
                            'value': 'name',
                            'ts': 0.8,
                            'end_ts': 1.1
                        },
                        {
                            'type': 'text',
                            'value': 'is',
                            'ts': 1.2,
                            'end_ts': 1.3
                        },
                        {
                            'type': 'text',
                            'value': 'Jack',
                            'ts': 1.4,
                            'end_ts': 1.7
                        }
                    ]
                }
            ]
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.get_result_object(JOB_ID)

        assert res == ForcedAlignmentResult(
            monologues=[
                Monologue(
                    speaker=0,
                    elements=[
                        ElementAlignment(value='Hi', ts=0.25, end_ts=0.5, type='text'),
                        ElementAlignment(value='my', ts=0.6, end_ts=0.75, type='text'),
                        ElementAlignment(value='name', ts=0.8, end_ts=1.1, type='text'),
                        ElementAlignment(value='is', ts=1.2, end_ts=1.3, type='text'),
                        ElementAlignment(value='Jack', ts=1.4, end_ts=1.7, type='text')
                    ]
                )
            ]
        )

        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=client.default_headers) 