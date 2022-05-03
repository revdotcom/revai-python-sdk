# -*- coding: utf-8 -*-
"""Sentiment analysis result model"""

from .sentiment_value import SentimentValue


class SentimentAnalysisResult:
    def __init__(self, messages):
        """
        :param messages: list of sentimented statements from the input in order of how they appeared
                         in the input.
        """
        self.messages = messages

    def __eq__(self, other):
        """Override default equality operator"""
        if isinstance(other, self.__class__):
            return all(a == b for a, b in zip(self.messages, other.messages))
        return False

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls([SentimentMessage.from_json(message) for message in json.get('messages', [])])


class SentimentMessage:
    def __init__(self, content, score, sentiment, timestamp=None, end_timestamp=None,
                 offset=None, length=None):
        """
        :param content: content of the informant, pulled from input
        :param score: Sentimental “score” of the content. Numbers less than 0 indicate a negative
                      (sad, angry) sentiment. Numbers above 0 indicate positive (joyful, happy)
                      sentiment
        :param: sentiment: Overall detected sentiment of the content, based off of score
        :param timestamp: time at which this element starts if input was json
        :param end_timestamp: time at which this element ends if input was json
        :param offset: Character index at which the content started in the source transcript,
                       excludes invisible characters
        :param length: Length of the content in characters, excludes invisible characters
        """
        self.content = content
        self.score = score
        self.sentiment = sentiment
        self.timestamp = timestamp
        self.end_timestamp = end_timestamp
        self.offset = offset
        self.length = length

    def __eq__(self, other):
        """Override default equality operator"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls(
            json['content'],
            json['score'],
            SentimentValue.from_string(json['sentiment']),
            json.get('ts'),
            json.get('end_ts'),
            json.get('offset'),
            json.get('length'))
