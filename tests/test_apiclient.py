# -*- coding: utf-8 -*-
"""Unit tests for RevAiApiClient"""

import pytest
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai import __version__


class TestRevAiAPIClient:
    def test_constructor_with_success(self):
        token = 'token'

        client = RevAiAPIClient(token)

        headers = client.session.headers

        assert headers.get('User-Agent') == 'python_sdk-{}'.format(__version__)
        assert headers.get('Authorization') == 'Bearer {}'.format(token)

    @pytest.mark.parametrize('token', [None, ''])
    def test_constructor_with_no_token(self, token):
        with pytest.raises(ValueError, match='access_token must be provided'):
            RevAiAPIClient(token)
