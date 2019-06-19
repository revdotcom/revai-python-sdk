# -*- coding: utf-8 -*-
"""Transcript model"""


class Transcript:
    def __init__(self, monologues):
        """
        :param monologues: list of monologues included in output
        """
        self.monologues = monologues

    def __eq__(self, other):
        """Override default equality operator"""
        if isinstance(other, self.__class__):
            return all(a == b for a, b in zip(self.monologues, other.monologues))
        return False

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls([Monologue.from_json(monologue) for monologue in json.get('monologues', [])])


class Monologue:
    def __init__(self, speaker, elements):
        """
        :param speaker: speaker identified for this monologue
        :param elements: list of elements spoken in this monologue
        """
        self.speaker = speaker
        self.elements = elements

    def __eq__(self, other):
        """Override default equality operator"""
        if isinstance(other, self.__class__):
            return all(a == b for a, b in zip(self.elements, other.elements)) \
                   and self.speaker == other.speaker
        return False

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls(
            json['speaker'],
            [Element.from_json(element) for element in json.get('elements', [])])


class Element:
    def __init__(self, type_, value, timestamp, end_timestamp, confidence):
        """
        :param type_: type of element: text, punct, or unknown
        :param value: value of the element
        :param timestamp: time at which this element starts in the audio
        :param end_timestamp: time at which this element ends in the audio
        :param confidence: confidence in this output
        """
        self.type_ = type_
        self.value = value
        self.timestamp = timestamp
        self.end_timestamp = end_timestamp
        self.confidence = confidence

    def __eq__(self, other):
        """Override default equality operator"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls(
            json['type'],
            json['value'],
            json.get('ts'),
            json.get('end_ts'),
            json.get('confidence'))
