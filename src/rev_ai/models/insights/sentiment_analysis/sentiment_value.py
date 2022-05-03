# -*- coding: utf-8 -*-
"""Enum for possible sentiments"""

from enum import Enum


class SentimentValue(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

    @classmethod
    def from_string(cls, status):
        return cls[status.upper()]
