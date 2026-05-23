# -*- coding: utf-8 -*-
"""Contains ForcedAlignmentResult dataclass"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ElementAlignment:
    """Dataclass containing information about an aligned word

    :param value: the word that was aligned
    :param ts: start time of the word in seconds
    :param end_ts: end time of the word in seconds
    :param type: type of element (always "text")
    """
    value: str
    ts: float
    end_ts: float
    type: str = "text"

    @staticmethod
    def from_json(json: Dict[str, Any]) -> 'ElementAlignment':
        """Creates an ElementAlignment from the given json dictionary

        :param json: json dictionary to convert
        :returns: ElementAlignment
        """
        return ElementAlignment(
            value=json.get('value'),
            ts=json.get('ts'),
            end_ts=json.get('end_ts'),
            type=json.get('type', 'text')
        )


@dataclass
class Monologue:
    """Dataclass containing information about a monologue section

    :param speaker: speaker identifier
    :param elements: list of words in this monologue with timing information
    """
    speaker: int
    elements: List[ElementAlignment]

    @staticmethod
    def from_json(json: Dict[str, Any]) -> 'Monologue':
        """Creates a Monologue from the given json dictionary

        :param json: json dictionary to convert
        :returns: Monologue
        """
        return Monologue(
            speaker=json.get('speaker', 0),
            elements=[ElementAlignment.from_json(element) for element in json.get('elements', [])]
        )


@dataclass
class ForcedAlignmentResult:
    """Dataclass containing the result of a forced alignment job

    :param monologues: A Monologue object per speaker containing the words
        they spoke with timing information
    """
    monologues: List[Monologue]

    @staticmethod
    def from_json(json: Dict[str, Any]) -> 'ForcedAlignmentResult':
        """Creates a ForcedAlignmentResult from the given json dictionary

        :param json: json dictionary to convert
        :returns: ForcedAlignmentResult
        """
        return ForcedAlignmentResult(
            monologues=[Monologue.from_json(monologue) for monologue in json.get('monologues', [])]
        ) 