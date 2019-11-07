# -*- coding: utf-8 -*-
"""Speech recognition tools for using Rev.ai"""

from . import CustomVocabulary


def _process_vocabularies(unprocessed_vocabularies):
    """
    This method takes in a list that contains CustomVocabulary objects
    and returns a list in which any such objects are converted properly
    to custom vocabulary dictionaries. Any items of other types in the list
    are not changed.
    """
    return list(map(lambda custom_vocabulary: custom_vocabulary.to_dict()
                    if isinstance(custom_vocabulary, CustomVocabulary)
                    else custom_vocabulary, unprocessed_vocabularies))
