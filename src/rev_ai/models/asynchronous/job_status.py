# -*- coding: utf-8 -*-
"""Enum for Job statuses"""

from enum import Enum


class JobStatus(str, Enum):
    IN_PROGRESS = 'in_progress'
    TRANSCRIBED = 'transcribed'
    FAILED = 'failed'
    COMPLETED = 'completed'

    @classmethod
    def from_string(cls, status):
        return cls[status.upper()]

    def __eq__(self, other):
        if isinstance(other, JobStatus):
            return self.value == other.value
        elif isinstance(other, str):
            return self.name.upper() == other.upper()
        else:
            return False
