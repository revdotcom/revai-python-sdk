# -*- coding: utf-8 -*-
"""Enum for Job statuses"""

from enum import Enum


class JobStatus(Enum):
    IN_PROGRESS = 1
    TRANSCRIBED = 2
    FAILED = 3
    COMPLETED = 4

    @classmethod
    def from_string(cls, status):
        return cls[status.upper()]
