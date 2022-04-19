# -*- coding: utf-8 -*-
"""Class for Custom Vocabulary model"""


class CustomVocabulary:
    """CustomVocabulary object to provide a clean way
    to create custom vocabularies. CustomVocabulary objects
    can be used in the various api clients."""

    def __init__(self, phrases):
        """Constructor

        :param phrases: list of strings of custom phrases to be recognized in
                        submitted audio
        """
        self.phrases = [phrase for phrase in phrases]

    def to_dict(self):
        """Returns the raw form of the custom vocabularies as the api
        expects them"""
        return {'phrases': self.phrases}
