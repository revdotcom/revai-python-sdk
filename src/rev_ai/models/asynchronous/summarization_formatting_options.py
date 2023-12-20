from enum import Enum
"""Summarization formatting options."""

class SummarizationFormattingOptions(str, Enum):
    PARAGRAPH = "paragraph"
    BULLETS = "bullets"
