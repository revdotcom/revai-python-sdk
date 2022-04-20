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

    def to_dict(self):
        """Returns the raw form of the transcript as the api
        returns them"""
        return {'monologues': [monologue.to_dict() for monologue in self.monologues]}

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls([Monologue.from_json(monologue) for monologue in json.get('monologues', [])])


class Monologue:
    def __init__(self, speaker, elements, speaker_info=None):
        """
        :param speaker: speaker identified for this monologue
        :param elements: list of elements spoken in this monologue
        :param speaker_info: information about the speaker if available
        """
        self.speaker = speaker
        self.elements = elements
        self.speaker_info = speaker_info

    def __eq__(self, other):
        """Override default equality operator"""
        if isinstance(other, self.__class__):
            return all(a == b for a, b in zip(self.elements, other.elements)) \
                and self.speaker == other.speaker \
                and self.speaker_info == other.speaker_info
        return False

    def to_dict(self):
        """Returns the raw form of the monologue as the api
        returns them"""
        json = {'speaker': self.speaker,
                'elements': [element.to_dict() for element in self.elements]}
        if self.speaker_info:
            json['speaker_info'] = self.speaker_info.to_dict()
        return json

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        speaker_info = None
        if json.get('speaker_info') is not None:
            speaker_info = SpeakerInfo.from_json(json['speaker_info'])
        return cls(
            json['speaker'],
            [Element.from_json(element) for element in json.get('elements', [])],
            speaker_info)


class SpeakerInfo:
    def __init__(self, id_, display_name):
        """
        :param id_: speaker id identified for this monologue
        :param display_name: Human readable name of the speaker if available
        """
        self.id = id_
        self.display_name = display_name

    def __eq__(self, other):
        """Override default equality operator"""
        if isinstance(other, self.__class__):
            return self.id == other.id and self.display_name == other.display_name
        return False

    def to_dict(self):
        """Returns the raw form of the monologue as the api
        returns them"""
        return {'id': self.id,
                'display_name': self.display_name}

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls(
            json['id'],
            json['display_name'])


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

    def to_dict(self):
        """Returns the raw form of the element as the api
        returns them"""
        return {'type': self.type_, 'value': self.value, 'ts': self.timestamp,
                'end_ts': self.end_timestamp, 'confidence': self.confidence}

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls(
            json['type'],
            json['value'],
            json.get('ts'),
            json.get('end_ts'),
            json.get('confidence'))
