# -*- coding: utf-8 -*-
"""Unit tests for RevAiApiClient"""

import pytest
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai import __version__
from src.rev_ai.models import RevAIBaseUrl

TOKEN = "token"


class TestRevAiAPIClient:
    def test_constructor_with_success(self):
        client = RevAiAPIClient(TOKEN)

        headers = client.default_headers

        assert headers.get('User-Agent') == 'RevAi-PythonSDK/{}'.format(__version__)
        assert headers.get('Authorization') == 'Bearer {}'.format(TOKEN)
        assert revai_base_url == RevAIBaseUrl.US.value

    def test_constructor_with_revai_base_url_success(self):
        client = RevAiAPIClient(TOKEN, RevAIBaseUrl.EU.value)

        headers = client.default_headers

        assert headers.get('User-Agent') == 'RevAi-PythonSDK/{}'.format(__version__)
        assert headers.get('Authorization') == 'Bearer {}'.format(TOKEN)
        assert revai_base_url == RevAIBaseUrl.EU.value

    @pytest.mark.parametrize('token', [None, ''])
    def test_constructor_with_no_token(self, token):
        with pytest.raises(ValueError, match='access_token must be provided'):
            RevAiAPIClient(token)
