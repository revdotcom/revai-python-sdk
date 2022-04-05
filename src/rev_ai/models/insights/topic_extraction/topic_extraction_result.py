# -*- coding: utf-8 -*-
"""Topic extraction result model"""


class TopicExtractionResult:
    def __init__(self, topics):
        """
        :param topics: list of topics included in output
        """
        self.topics = topics

    def __eq__(self, other):
        """Override default equality operator"""
        if isinstance(other, self.__class__):
            return all(a == b for a, b in zip(self.topics, other.topics))
        return False

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls([Topic.from_json(topic) for topic in json.get('topics', [])])


class Topic:
    def __init__(self, topic_name, score, informants):
        """
        :param topic_name: name of the topic, pulled directly from somewhere in the input text
        :param score: score of the topic, between 0 and 1. Higher means it is more likely that this
                      is truly a topic
        :param informants: pieces of the input text which informed this choice of topic
        """
        self.topic_name = topic_name
        self.score = score
        self.informants = informants

    def __eq__(self, other):
        """Override default equality operator"""
        if isinstance(other, self.__class__):
            return all(a == b for a, b in zip(self.informants, other.informants)) \
                and self.topic_name == other.topic_name \
                and self.score == other.score
        return False

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls(
            json['topic_name'],
            json['score'],
            [Informant.from_json(informant) for informant in json.get('informants', [])])


class Informant:
    def __init__(self, content, timestamp=None, end_timestamp=None, offset=None, length=None):
        """
        :param content: content of the informant, pulled from input
        :param timestamp: time at which this element starts if input was json
        :param end_timestamp: time at which this element ends if input was json
        :param offset: Character index at which the content started in the source transcript,
                       excludes invisible characters
        :param length: Length of the content in characters, excludes invisible characters
        """
        self.content = content
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
            json.get('ts'),
            json.get('end_ts'),
            json.get('offset'),
            json.get('length'))
