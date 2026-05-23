# -*- coding: utf-8 -*-
"""Client used for interacting with our forced alignment api"""

import json
from .generic_api_client import GenericApiClient
from .models.forced_alignment import ForcedAlignmentJob, ForcedAlignmentResult


class ForcedAlignmentClient(GenericApiClient):
    """Client for interacting with the Rev AI forced alignment api"""

    # Default version of Rev AI forced alignment api
    api_version = 'v1'

    # Default api name of Rev AI forced alignment api
    api_name = 'alignment'

    def __init__(self, access_token):
        """Constructor

        :param access_token: access token which authorizes all requests and links them to your
                             account. Generated on the settings page of your account dashboard
                             on Rev AI.
        """
        GenericApiClient.__init__(self, access_token, self.api_name, self.api_version,
                                  ForcedAlignmentJob.from_json, ForcedAlignmentResult.from_json)

    def submit_job_url(
            self,
            source_config=None,
            source_transcript_config=None,
            transcript_text=None,
            metadata=None,
            delete_after_seconds=None,
            notification_config=None,
            language=None):
        """Submit a job to the Rev AI forced alignment api.

        :param source_config: CustomerUrlData object containing url of the source media and
            optional authentication headers to use when accessing the source url
        :param source_transcript_config: CustomerUrlData object containing url of the transcript file and
            optional authentication headers to use when accessing the transcript url
        :param transcript_text: The text of the transcript to be aligned (no punctuation, just words)
        :param metadata: info to associate with the alignment job
        :param delete_after_seconds: number of seconds after job completion when job is auto-deleted
        :param notification_config: CustomerUrlData object containing the callback url to
            invoke on job completion as a webhook and optional authentication headers to use when
            calling the callback url
        :param language: Language code for the audio and transcript. One of: "en", "es", "fr"
        :returns: ForcedAlignmentJob object
        :raises: HTTPError
        """
        if not source_config:
            raise ValueError('source_config must be provided')
        if not (source_transcript_config or transcript_text):
            raise ValueError('Either source_transcript_config or transcript_text must be provided')
        if source_transcript_config and transcript_text:
            raise ValueError('Only one of source_transcript_config or transcript_text may be provided')

        payload = self._enhance_payload({
            'source_config': source_config.to_dict() if source_config else None,
            'source_transcript_config': source_transcript_config.to_dict() if source_transcript_config else None,
            'transcript_text': transcript_text,
            'language': language
        }, metadata, None, delete_after_seconds, notification_config)

        return self._submit_job(payload)

    def get_result_json(self, id_):
        """Get result of a forced alignment job as json.

        :param id_: id of job to be requested
        :returns: job result data as raw json
        :raises: HTTPError
        """
        return self._get_result_json(id_, {}, route='transcript')

    def get_result_object(self, id_):
        """Get result of a forced alignment job as ForcedAlignmentResult object.

        :param id_: id of job to be requested
        :returns: job result data as ForcedAlignmentResult object
        :raises: HTTPError
        """
        return self._get_result_object(id_, {}, route='transcript')