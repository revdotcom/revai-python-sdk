# -*- coding: utf-8 -*-
"""Enum for transcript content types"""

from enum import Enum


class TranscriptType(Enum):
    JSON = "application/vnd.rev.transcript.v1.0+json"
    TEXT = "text/plain"

    @classmethod
    def from_string(cls, status):
        return cls[status.upper()]
