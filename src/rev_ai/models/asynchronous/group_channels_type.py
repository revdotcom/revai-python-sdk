# -*- coding: utf-8 -*-
"""Enum for caption content types"""

from enum import Enum


class GroupChannelsType(Enum):
    SPEAKER = 'speaker'
    SENTENCE = 'sentence'
    WORD = 'word'

    @classmethod
    def from_string(cls, status):
        return cls[status.upper()]
