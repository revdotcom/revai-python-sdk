# -*- coding: utf-8 -*-
"""Unit tests for Rev Ai Utils"""
import pytest

from src.rev_ai.utils import _process_vocabularies, check_exclusive_options
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

    def test_check_exclusive_options(self):
        option1 = "opt1"
        option2 = "opt2"
        option1_name = "name1"
        option2_name = "name2"
        # test either option
        check_exclusive_options(None, option1_name, option2, option2_name)
        check_exclusive_options(option1, option1_name, None, option2_name)
        # Raise error if both
        with pytest.raises(ValueError) as err:
            check_exclusive_options(option1, option1_name, option2, option2_name)
        assert "Only one of {0} or {1} may be provided".format(option1_name, option2_name) in \
               str(err.value)
