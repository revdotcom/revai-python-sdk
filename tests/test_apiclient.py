# -*- coding: utf-8 -*-
"""Unit tests for RevAiApiClient"""

import pytest
from src.rev_ai.apiclient import RevAiAPIClient


class TestRevAiAPIClient:
    def test_constructor_success(self):
        token = 'key'

        client = RevAiAPIClient(token)

        headers = client.session.headers
        assert headers.get('User-Agent') == 'python_sdk'
        assert headers.get('Authorization') == 'Bearer {}'.format(token)

    @pytest.mark.parametrize("token", [None, ""])
    def test_constructor_invalid_token_produces_error(self, token):
        with pytest.raises(ValueError, match='API Key cannot be empty.'):
            RevAiAPIClient(token)
