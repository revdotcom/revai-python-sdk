# -*- coding: utf-8 -*-
"""Client used or interacting with our language identification api"""

import json
from .generic_api_client import GenericApiClient
from .models import LanguageIdentificationJob, LanguageIdentificationResult

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class LanguageIdentificationClient(GenericApiClient):
    """Client for interacting with the Rev AI language identification api"""

    # Default version of Rev AI language identification api
    api_version = 'v1'

    # Default api name of Rev AI language identification api
    api_name = 'languageid'

    def __init__(self, access_token):
        """Constructor

        :param access_token: access token which authorizes all requests and links them to your
                             account. Generated on the settings page of your account dashboard
                             on Rev AI.
        """

        GenericApiClient.__init__(self, access_token, self.api_name, self.api_version,
                                  LanguageIdentificationJob.from_json,
                                  LanguageIdentificationResult.from_json)

    def submit_job_url(
            self,
            media_url,
            metadata=None,
            callback_url=None,
            delete_after_seconds=None,
            source_config=None,
            notification_config=None):
        """Submit media as a URL for language identification.
        The audio data is downloaded from the URL.

        :param media_url: web location of the media file
        .. deprecated:: 2.16.0
            Use source_config instead
        :param metadata: info to associate with the language identification job
        :param callback_url: callback url to invoke on job completion as a webhook
        .. deprecated:: 2.16.0
                Use notification_config instead
        :param delete_after_seconds: number of seconds after job completion when job is auto-deleted
        :param source_config: CustomerUrlData object containing url of the source media and
            optional authentication headers to use when accessing the source url
        :param notification_config: CustomerUrlData object containing the callback url to
            invoke on job completion as a webhook and optional authentication headers to use when
            calling the callback url
        :returns: raw response data
        :raises: HTTPError
        """
        payload = self.create_payload_with_source(media_url, source_config, metadata, callback_url,
                                                  delete_after_seconds, notification_config)

        return self._submit_job(payload)

    def submit_job_local_file(
            self,
            filename,
            metadata=None,
            callback_url=None,
            delete_after_seconds=None,
            notification_config=None):
        """Submit a local file for language identification.
        Note that the content type is inferred if not provided.

        :param filename: path to a local file on disk
        :param metadata: info to associate with the language identification job
        :param callback_url: callback url to invoke on job completion as a webhook
        :param delete_after_seconds: number of seconds after job completion when job is auto-deleted
        :param notification_config: CustomerUrlData object containing the callback url to
            invoke on job completion as a webhook and optional authentication headers to use when
            calling the callback url
        :returns: raw response data
        :raises: HTTPError
        """
        if not filename:
            raise ValueError('filename must be provided')

        payload = self._enhance_payload({}, metadata, callback_url, delete_after_seconds,
                                        notification_config)

        with open(filename, 'rb') as f:
            files = {
                'media': (filename, f),
                'options': (None, json.dumps(payload, sort_keys=True))
            }

            response = self._make_http_request(
                "POST",
                urljoin(self.base_url, 'jobs'),
                files=files
            )

        return LanguageIdentificationJob.from_json(response.json())

    def get_result_json(self, id_):
        """Get result of a language identification job as json.

        :param id_: id of job to be requested
        :returns: job result data as raw json
        :raises: HTTPError
        """
        return self._get_result_json(id_, {})

    def get_result_object(self, id_):
        """Get result of a language identification job as LanguageIdentificationResult object.

        :param id_: id of job to be requested
        :returns: job result data as LanguageIdentificationResult object
        :raises: HTTPError
        """
        return self._get_result_object(id_, {})
