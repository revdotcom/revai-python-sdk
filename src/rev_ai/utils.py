# -*- coding: utf-8 -*-
"""Speech recognition tools for using Rev AI"""

from . import CustomVocabulary
from . import SpeakerName


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


def _process_speaker_names(unprocessed_speaker_names):
    """
    This method takes in a list that contains SpeakerName objects
    and returns a list in which any such objects are converted properly
    to speaker name dictionaries. Any items of other types in the list
    are not changed.
    """
    return list(map(lambda speaker_name: speaker_name.to_dict()
                    if isinstance(speaker_name, SpeakerName)
                    else speaker_name, unprocessed_speaker_names))
