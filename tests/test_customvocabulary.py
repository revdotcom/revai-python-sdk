# -*- coding: utf-8 -*-
"""Unit tests for custom vocabulary"""
from src.rev_ai.custom_vocabularies_client import RevAiCustomVocabulariesClient
from src.rev_ai.models import CustomVocabulary

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

TOKEN = "token"
CV_ID = "cv1"
PHRASES = ["Patrick Henry Winston", "Noam Chomsky"]


class TestCustomVocabulary():

    def test_constructor(self):
        custom_vocabulary = CustomVocabulary(PHRASES)

        assert custom_vocabulary.phrases == PHRASES

    def test_no_aliasing_phrases_list(self):
        alias = [phrase for phrase in PHRASES]
        custom_vocabulary = CustomVocabulary(alias)

        alias.pop()

        assert len(custom_vocabulary.phrases) == 2
        assert custom_vocabulary.phrases == PHRASES

    def test_to_dict_method(self):
        custom_vocabulary = CustomVocabulary(PHRASES)

        custom_vocabulary_dict = custom_vocabulary.to_dict()

        assert custom_vocabulary_dict == {'phrases': PHRASES}


class TestCustomVocabularyEndpoints():
    def test_get_custom_vocabularies_information_success(self, mock_session, make_mock_response):
        data = {
            'id': CV_ID,
            'status': 'complete',
            'created_on': '2018-05-05T23:23:22.29Z'
        }
        client = RevAiCustomVocabulariesClient(TOKEN)
        url = urljoin(client.base_url, CV_ID)
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.get_custom_vocabularies_information(CV_ID)

        assert res == data
        mock_session.request.assert_called_once_with("GET", url,
                                                     headers=client.default_headers)

    def test_get_list_of_custom_vocabularies_success(self, mock_session, make_mock_response):
        data = {
            'id': CV_ID,
            'status': 'complete',
            'created_on': '2018-05-05T23:23:22.29Z'
        }
        client = RevAiCustomVocabulariesClient(TOKEN)
        response = make_mock_response(url=client.base_url, json_data=[data])
        mock_session.request.return_value = response

        res = client.get_list_of_custom_vocabularies()

        assert res == [data]
        mock_session.request.assert_called_once_with("GET", client.base_url,
                                                     headers=client.default_headers)

    def test_get_list_of_custom_vocabularies_with_limit(self, mock_session, make_mock_response):
        data = {
            'id': CV_ID,
            'status': 'complete',
            'created_on': '2018-05-05T23:23:22.29Z'
        }
        limit = 5
        client = RevAiCustomVocabulariesClient(TOKEN)
        url = '{}?limit={}'.format(client.base_url, limit)
        response = make_mock_response(url=client.base_url, json_data=[data])
        mock_session.request.return_value = response

        res = client.get_list_of_custom_vocabularies(limit)

        assert res == [data]
        mock_session.request.assert_called_once_with("GET", url,
                                                     headers=client.default_headers)

    def test_delete_custom_vocabulary_success(self, mock_session, make_mock_response):
        client = RevAiCustomVocabulariesClient(TOKEN)
        url = urljoin(client.base_url, CV_ID)
        response = make_mock_response(url=url, status=204)
        mock_session.request.return_value = response

        res = client.delete_custom_vocabulary(CV_ID)

        assert res is None
        mock_session.request.assert_called_once_with("DELETE", url,
                                                     headers=client.default_headers)
