# -*- coding: utf-8 -*-
"""Speech recognition tools for using Rev.ai"""

from .baseclient import BaseClient
from . import utils

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class RevAiCustomVocabulariesClient(BaseClient):
    """Client which implements Rev.ai CustomVocabulary API"""

    def __init__(self, access_token):
        """Constructor

        :param access_token: access token which authorizes all requests and
                             links them to your account. Generated on the
                             settings page of your account dashboard
                             on Rev.ai
        """
        BaseClient.__init__(self, access_token)

        self.base_url = urljoin(self.base_url, 'vocabularies/')

    def submit_custom_vocabularies(
            self,
            custom_vocabularies,
            callback_url=None,
            metadata=None):
        """Submit custom vocabularies.

        :param custom_vocabularies: List of CustomVocabulary objects
        :param callback_url: callback url to invoke on job completion as a
                             webhook
        :param metadata: info to associate with the transcription job
        """

        if not custom_vocabularies:
            raise ValueError('custom_vocabularies must be provided')

        payload = self._create_custom_vocabularies_options_payload(
            custom_vocabularies,
            callback_url,
            metadata
        )

        response = self._make_http_request(
            "POST",
            self.base_url,
            json=payload
        )

        return response.json()

    def get_custom_vocabularies_information(
            self,
            id):
        """ Get the custom vocabulary status
        :param id: string id of custom vocabulary submission
        """

        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, "{}".format(id))
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
            payload['custom_vocabularies'] =\
                utils._process_vocabularies(custom_vocabularies)
        return payload
