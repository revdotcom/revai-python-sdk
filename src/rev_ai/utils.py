# -*- coding: utf-8 -*-
"""Speech recognition tools for using Rev.ai"""

from . import CustomVocabulary


def _process_vocabularies(unprocessed_vocabularies):
    return list(map(lambda custom_vocabulary: custom_vocabulary.to_dict()
                    if isinstance(custom_vocabulary, CustomVocabulary)
                    else custom_vocabulary, unprocessed_vocabularies))


def _validate_custom_vocabularies(custom_vocabularies_list):
    for custom_vocabulary in custom_vocabularies_list:
        if len(custom_vocabulary.keys()) != 1 or 'phrases' not in custom_vocabulary.keys():
            raise ValueError("Custom vocabularies malformed, must be dict with \
                'phrases' as key")
