# -*- coding: utf-8 -*-
"""Speech recognition tools for using Rev AI"""

from .baseclient import BaseClient
from . import utils
from .models.customer_url_data import CustomerUrlData

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class RevAiCustomVocabulariesClient(BaseClient):
    """Client which implements Rev AI CustomVocabulary API
    See https://docs.rev.ai/api/custom-vocabulary/reference/
    """

    # Default version of Rev AI
    version = 'v1'

    # Default base url for Rev AI
    base_url = 'https://api.rev.ai/speechtotext/{}/'.format(version)

    def __init__(self, access_token):
        """Constructor

        :param access_token: access token which authorizes all requests and
                             links them to your account. Generated on the
                             settings page of your account dashboard
                             on Rev AI
        """
        BaseClient.__init__(self, access_token)

        self.base_url = urljoin(self.base_url, 'vocabularies/')

    def submit_custom_vocabularies(
            self,
            custom_vocabularies,
            callback_url=None,
            metadata=None,
            notification_config=None):
        """Submit custom vocabularies.
        See https://docs.rev.ai/api/custom-vocabulary/reference/#operation/SubmitCustomVocabulary
        :param custom_vocabularies: List of CustomVocabulary objects
        :param callback_url: callback url to invoke on job completion as a webhook
        .. deprecated:: 2.16.0
                Use notification_config instead
        :param metadata: info to associate with the transcription job
        :param notification_config: CustomerUrlData object containing the callback url to
            invoke on job completion as a webhook and optional authentication headers to use when
            calling the callback url
        """

        if not custom_vocabularies:
            raise ValueError('custom_vocabularies must be provided')

        payload = self._create_custom_vocabularies_options_payload(
            custom_vocabularies,
            callback_url,
            metadata,
            notification_config
        )

        response = self._make_http_request(
            "POST",
            self.base_url,
            json=payload
        )

        return response.json()

    def get_custom_vocabularies_information(self, id):
        """ Get the custom vocabulary status
        See https://docs.rev.ai/api/custom-vocabulary/reference/#operation/GetCustomVocabulary

        :param id: string id of custom vocabulary submission
        """

        response = self._make_http_request("GET", urljoin(self.base_url, id))
        return response.json()

    def get_list_of_custom_vocabularies(self, limit=None):
        """ Get a list of custom vocabularies
        See https://docs.rev.ai/api/custom-vocabulary/reference/#operation/GetCustomVocabularies

        :param limit: optional, limits the number of jobs returned
        """

        url = self.base_url
        if limit:
            url += '?limit={}'.format(limit)

        response = self._make_http_request("GET", url)
        return response.json()

    def delete_custom_vocabulary(self, id):
        """ Delete a custom vocabulary
        See https://docs.rev.ai/api/custom-vocabulary/reference/#operation/DeleteCustomVocabulary

        :param id: string id of custom vocabulary to be deleted
        :returns: None if job was successfully deleted
        :raises: HTTPError
        """

        self._make_http_request("DELETE", urljoin(self.base_url, id))
        return

    def _create_custom_vocabularies_options_payload(
            self,
            custom_vocabularies,
            callback_url=None,
            metadata=None,
            notification_config=None):
        payload = {}
        if custom_vocabularies:
            payload['custom_vocabularies'] = utils._process_vocabularies(custom_vocabularies)
        if callback_url:
            payload['callback_url'] = callback_url
        if metadata:
            payload['metadata'] = metadata
        if notification_config:
            payload['notification_config'] = notification_config.to_dict()
        return payload
