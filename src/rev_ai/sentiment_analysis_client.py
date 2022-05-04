# -*- coding: utf-8 -*-
"""Client used or interacting with out sentiment analysis api"""

from .generic_api_client import GenericApiClient
from .models import SentimentAnalysisJob, SentimentAnalysisResult


class SentimentAnalysisClient(GenericApiClient):
    """Client for interacting with the Rev AI sentiment analysis api"""

    # Default version of Rev AI sentiment analysis api
    api_version = 'v1'

    # Default api name of Rev AI sentiment analysis api
    api_name = 'sentiment_analysis'

    def __init__(self, access_token):
        """Constructor

        :param access_token: access token which authorizes all requests and links them to your
                             account. Generated on the settings page of your account dashboard
                             on Rev AI.
        """

        GenericApiClient.__init__(self, access_token, self.api_name, self.api_version,
                                  SentimentAnalysisJob.from_json, SentimentAnalysisResult.from_json)

    def submit_job_from_text(self,
                             text=None,
                             metadata=None,
                             callback_url=None,
                             delete_after_seconds=None,
                             language=None,
                             notification_config=None):
        """Submit a job to the Rev AI sentiment analysis api. Takes either a plain text string or
        Transcript object

        :param text: Plain text string to be run through sentiment analysis
        :param metadata: info to associate with the transcription job
        :param callback_url: callback url to invoke on job completion as
                             a webhook
        :param delete_after_seconds: number of seconds after job completion when job is auto-deleted
        :param language: specify language using the one of the supported ISO 639-1 (2-letter) or
            ISO 639-3 (3-letter) language codes as defined in the API Reference
        :param notification_config: CustomerUrlData object containing the callback url to
            invoke on job completion as a webhook and optional authentication headers to use when
            calling the callback url
        :returns: SentimentAnalysisJob object
        :raises: HTTPError
        """
        payload = self._enhance_payload({'text': text, 'language': language},
                                        metadata, callback_url, delete_after_seconds,
                                        notification_config)
        return self._submit_job(payload)

    def submit_job_from_transcript(self,
                                   transcript=None,
                                   metadata=None,
                                   callback_url=None,
                                   delete_after_seconds=None,
                                   language=None,
                                   notification_config=None):
        """Submit a job to the Rev AI sentiment analysis api. Takes either a plain text string or
        Transcript object

        :param transcript: Transcript object from the Rev AI async transcription client to be run
                           through sentiment analysis
        :param metadata: info to associate with the transcription job
        :param callback_url: callback url to invoke on job completion as
                             a webhook
        :param delete_after_seconds: number of seconds after job completion when job is auto-deleted
        :param language: specify language using the one of the supported ISO 639-1 (2-letter) or
            ISO 639-3 (3-letter) language codes as defined in the API Reference
        :param notification_config: CustomerUrlData object containing the callback url to
            invoke on job completion as a webhook and optional authentication headers to use when
            calling the callback url
        :returns: SentimentAnalysisJob object
        :raises: HTTPError
        """
        payload = self._enhance_payload({'json': transcript.to_dict(), 'language': language},
                                        metadata, callback_url, delete_after_seconds,
                                        notification_config)
        return self._submit_job(payload)

    def get_result_json(self, id_, filter_for=None):
        """Get result of a sentiment analysis job as json.

        :param id_: id of job to be requested
        :param filter_for: SentimentValue to filter for.
                           If specified only sentiments of this type will be returned
        :returns: job result data as raw json
        :raises: HTTPError
        """
        to_filter_for = str(filter_for) if filter_for else None
        return self._get_result_json(id_, {'filter_for': to_filter_for})

    def get_result_object(self, id_, filter_for=None):
        """Get result of a sentiment analysis job as SentimentAnalysisResult object.

        :param id_: id of job to be requested
        :param filter_for: SentimentValue to filter for.
                           If specified only sentiments of this type will be returned
        :returns: job result data as SentimentAnalysisResult object
        :raises: HTTPError
        """
        to_filter_for = str(filter_for) if filter_for else None
        return self._get_result_object(id_, {'filter_for': to_filter_for})
