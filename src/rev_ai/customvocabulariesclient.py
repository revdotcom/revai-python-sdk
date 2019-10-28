# -*- coding: utf-8 -*-
"""Speech recognition tools for using Rev.ai"""

import requests
import json
from requests.exceptions import HTTPError
# from .models import Job, Account, Transcript, CaptionType
from . import __version__

try:
    from urllib.parse import urljoin
except:
    from urlparse import urljoin


class RevAiCustomVocabulariesClient:
    """Client which implements Rev.ai CustomVocabulary API"""

    # Default version of Rev.ai
    version = 'v1'

    # Default address of the API
    base_url = 'https://api.rev.ai/speechtotext/{}/vocabularies'.format(
        version)

    def __init__(self, access_token):
        """Constructor

        :param access_token: access token which authorizes all requests and
                             links them to your account. Generated on the
                             settings page of your account dashboard
                             on Rev.ai
        """
        if not access_token:
            raise ValueError('access_token must be provided')

        self.default_headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            'User-Agent': 'RevAi-PythonSDK/{}'.format(__version__)
        }

    def submit_custom_vocabularies(
            self,
            custom_vocabularies,
            callback_url=None,
            metadata=None):
        """Submit custom vocabularies.

        :param custom_vocabularies: List of objects containing phrases list
        :param callback_url: callback url to invoke on job completion as a
                             webhook
        :param metadata: info to associate with the transcription job
        """

        if not custom_vocabularies:
            raise ValueError('custom_vocabularies must be provided')

        payload = self._create_custom_vocabularies_options_payload(
            callback_url,
            metadata,
            custom_vocabularies
        )

        response = self._make_http_request(
            "POST",
            self.base_url,
            json=payload
        )

        return response.json()

    def get_custom_vocabularies(
            self,
            id):
        """ Get the custom vocabulary status
        :param id: string id of custom vocabulary submission
        """

        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, "vocabularies/{}/".format(id))
        )

        return response.json()

    def _create_custom_vocabularies_options_payload(
            self,
            custom_vocabularies,
            callback_url=None,
            metadata=None):
        payload = {}
        if callback_url:
            payload['callback_url'] = callback_url
        if metadata:
            payload['metadata'] = metadata
        if custom_vocabularies:
            payload['custom_vocabularies'] = custom_vocabularies
        return payload

    def _make_http_request(self, method, url, **kwargs):
        """Wrapper method for initiating HTTP requests and handling potential
            errors.

        :param method: string of HTTP method request
        :param url: string containing the URL to make the request to
        :param (optional) **kwargs: potential extra arguments including header
            and stream
        :raises: HTTPError
        """
        headers = self.default_headers.copy()
        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
            del kwargs['headers']
        with requests.Session() as session:
            response = session.request(method, url, headers=headers, **kwargs)

        try:
            response.raise_for_status()
            return response
        except HTTPError as err:
            if (response.content):
                err.args = (err.args[0] +
                            "; Server Response : {}".
                            format(response.content.decode('utf-8')),)
            raise
