# -*- coding: utf-8 -*-
"""Speaker name model"""


class SpeakerName:
    """SpeakerName object to provide a clean way
    to pass speaker names to human transcription"""

    def __init__(self, display_name):
        """Constructor

        :param display_name: human readable string representing the speaker's name
        """
        self.display_name = display_name

    def to_dict(self):
        """Returns the raw form of the speaker name as the api
        expects it"""
        return {'display_name': self.display_name}
