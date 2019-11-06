# -*- coding: utf-8 -*-
"""Unit tests for RevAi Utils"""

from src.rev_ai.models import CustomVocabulary

phrases = ["Patrick Henry Winston", "Noam Chomsky"]


class TestCustomVocabulary:

    def test_constructor(self):
        custom_vocabulary = CustomVocabulary(phrases)

        assert custom_vocabulary.phrases == phrases

    def test_no_aliasing_phrases_list(self):
        alias = [phrase for phrase in phrases]
        custom_vocabulary = CustomVocabulary(alias)

        alias.pop()

        assert len(custom_vocabulary.phrases) == 2
        assert custom_vocabulary.phrases == phrases

    def test_to_dict_method(self):
        custom_vocabulary = CustomVocabulary(phrases)

        custom_vocabulary_dict = custom_vocabulary.to_dict()

        assert custom_vocabulary_dict == {'phrases': phrases}
