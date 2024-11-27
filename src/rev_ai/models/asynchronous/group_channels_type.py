# -*- coding: utf-8 -*-
"""Enum for group_channels_by types"""

from enum import Enum


class GroupChannelsType(str, Enum):
    SPEAKER = 'speaker'
    SENTENCE = 'sentence'
    WORD = 'word'

    @classmethod
    def from_string(cls, status):
        return cls[status.upper()]
