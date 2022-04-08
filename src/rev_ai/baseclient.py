# -*- coding: utf-8 -*-
"""Speech recognition tools for using Rev AI"""

import requests
from requests.exceptions import HTTPError
from . import __version__
from . import CustomVocabulary


class BaseClient:
    """Base for client's making HTTP Requests to Rev AI Apis"""

    def __init__(self, access_token):
        """Constructor

        :param access_token: access token which authorizes all requests and
                             links them to your account. Generated on the
                             settings page of your account dashboard
                             on Rev AI
        """
        if not access_token:
            raise ValueError('access_token must be provided')

        self.default_headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            'User-Agent': 'RevAi-PythonSDK/{}'.format(__version__)
        }

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
