# -*- coding: utf-8 -*-
from enum import Enum


class TranslationJobStatus(str, Enum):
    """Enum for Translation Job statuses"""
    IN_PROGRESS = "in_progress"
    FAILED = "failed"
    COMPLETED = "completed"
