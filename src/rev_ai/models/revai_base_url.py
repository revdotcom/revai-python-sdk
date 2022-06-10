# -*- coding: utf-8 -*-
"""Enum for Rev AI base urls across deployments"""

from enum import Enum


class RevAIBaseUrl(Enum):
    US = "https://api.rev.ai"
    EU = "https://ec1.api.rev.ai"

    @classmethod
    def from_string(cls, status):
        return cls[status.upper()]