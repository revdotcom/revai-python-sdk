# -*- coding: utf-8 -*-
"""Unit tests for Rev Ai Utils"""

from src.rev_ai.utils import _process_vocabularies
from src.rev_ai.models import CustomVocabulary

phrases = ["Patrick Henry Winston", "Noam Chomsky"]
other_phrases = ['Steve Jobs']


class TestUtils:
    def test_process_vocabularies_with_custom_vocab_dict(self):
        customvocabs = [{'phrases': phrases}]

        processed_vocabs = _process_vocabularies(customvocabs)

        assert processed_vocabs == [{'phrases': phrases}]

    def test_process_vocabularies_with_CustomVocabulary_instance(self):
        customvocabs = [CustomVocabulary(phrases)]

        processed_vocabs = _process_vocabularies(customvocabs)

        assert processed_vocabs == [{'phrases': phrases}]

    def test_process_vocabularies_with_mixed_input(self):
        customvocabs = [CustomVocabulary(phrases), {'phrases': other_phrases}]

        processed_vocabs = _process_vocabularies(customvocabs)

        assert processed_vocabs == [{'phrases': phrases}, {'phrases': other_phrases}]

    def test_process_vocabularies_with_empty_list(self):
        processed_vocabs = _process_vocabularies([])

        assert processed_vocabs == []
