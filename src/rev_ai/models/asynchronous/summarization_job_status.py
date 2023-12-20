# -*- coding: utf-8 -*-
"""Enum for Job statuses"""

from enum import Enum


class SummarizationJobStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    FAILED = "failed"
    COMPLETED = "completed"
