# -*- coding: utf-8 -*-
"""Language identification result model"""


class LanguageIdentificationResult:
    def __init__(self, top_language, language_confidences):
        """
        :param top_language: Language code of predicted language
        :param language_confidences: List of all potential languages with their corresponding
            confidence scores
        """
        self.top_language = top_language
        self.language_confidences = language_confidences

    def __eq__(self, other):
        """Override default equality operator"""
        if isinstance(other, self.__class__):
            return all(a == b for a, b in
                       zip(self.language_confidences, other.language_confidences)) \
                and self.top_language == other.top_language
        return False

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls(
            json['top_language'],
            [LanguageConfidence.from_json(language_confidence) for
             language_confidence in json.get('language_confidences', [])])


class LanguageConfidence:
    def __init__(self, language, confidence):
        """
        :param language: Language code of predicted language
        :param confidence: Confidence score of the predicted language, ranges from 0.00 to 1.00
        """
        self.language = language
        self.confidence = confidence

    def __eq__(self, other):
        """Override default equality operator"""
        if isinstance(other, self.__class__):
            return self.language == other.language and self.confidence == other.confidence
        return False

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls(
            json['language'],
            json['confidence'])
