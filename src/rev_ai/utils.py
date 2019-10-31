# -*- coding: utf-8 -*-
"""Speech recognition tools for using Rev.ai"""

from . import CustomVocabulary


def _process_vocabularies(unprocessed_vocabularies):
    return list(map(lambda custom_vocabulary: custom_vocabulary.to_dict()
                    if isinstance(custom_vocabulary, CustomVocabulary)
                    else custom_vocabulary, unprocessed_vocabularies))
