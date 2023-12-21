from enum import Enum


class SummarizationFormattingOptions(str, Enum):
    """Summarization formatting options."""
    PARAGRAPH = "paragraph"
    BULLETS = "bullets"
