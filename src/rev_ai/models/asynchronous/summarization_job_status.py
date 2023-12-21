# -*- coding: utf-8 -*-
from enum import Enum


class SummarizationJobStatus(str, Enum):
    """Enum for Summarization Job statuses"""
    IN_PROGRESS = "in_progress"
    FAILED = "failed"
    COMPLETED = "completed"
