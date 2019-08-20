# -*- coding: utf-8 -*-
"""Enum for caption content types"""

from enum import Enum


class CaptionType(Enum):
    SRT = "application/x-subrip"
    VTT = "text/vtt"

    @classmethod
    def from_string(cls, status):
        return cls[status.upper()]
