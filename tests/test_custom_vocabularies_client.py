import pytest
import re
import json
from requests.exceptions import HTTPError
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai import __version__
from src.rev_ai.custom_vocabularies_client import RevAiCustomVocabulariesClient
from tests.helpers.errors import get_error_test_cases

TOKEN = "token"


class TestCustomVocabulariesClient:
    def test_constructor_with_success(self):
        client = RevAiCustomVocabulariesClient(TOKEN)

        headers = client.default_headers

        assert headers.get(
            'User-Agent') == 'RevAi-PythonSDK/{}'.format(__version__)
        assert headers.get('Authorization') == 'Bearer {}'.format(TOKEN)

    @pytest.mark.parametrize('token', [None, ''])
    def test_constructor_with_no_token(self, token):
        with pytest.raises(ValueError, match='access_token must be provided'):
            RevAiAPIClient(token)
