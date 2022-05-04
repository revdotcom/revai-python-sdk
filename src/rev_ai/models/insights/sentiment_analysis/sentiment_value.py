# -*- coding: utf-8 -*-
"""Enum for possible sentiments"""

from enum import Enum


class SentimentValue(Enum):
    POSITIVE = 1
    NEGATIVE = 2
    NEUTRAL = 3

    def __str__(self):
        return self.name.lower()

    @classmethod
    def from_string(cls, status):
        return cls[status.upper()]
