import pytest
from src.rev_ai import __version__
from src.rev_ai.custom_vocabularies_client import RevAiCustomVocabulariesClient

try:
    from unittest import mock
except ImportError:
    import mock

TOKEN = "token"


class TestCustomVocabulariesClient:
    def test_constructor_with_success(self):
        client = RevAiCustomVocabulariesClient(TOKEN)

        headers = client.default_headers

        assert headers.get(
            'User-Agent') == 'RevAi-PythonSDK/{}'.format(__version__)
        assert headers.get('Authorization') == 'Bearer token'
        assert client.base_url == 'https://api.rev.ai/speechtotext/v1/vocabularies/'

    @pytest.mark.parametrize('token', [None, ''])
    def test_constructor_with_no_token(self, token):
        with pytest.raises(ValueError, match='access_token must be provided'):
            RevAiCustomVocabulariesClient(token)
