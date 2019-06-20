# -*- coding: utf-8 -*-
"""Media Config Model """


class MediaConfig:
    def __init__(self, content_type='audio/*', layout=None, rate=None,
                 audio_format=None, channels=None):
        """Constructor for MediaConfig class

        :param content_type (optional): string containing content type. Default
            will resort to 'audio/*'
        :param layout (optional): layout of audio
        :param rate (optional): sampling rate of audio
        :param audio_format (optional): format of audio
        :param channels (optional): the number of channels the audio has
        """
        self.content_type = content_type
        self.layout = layout
        self.rate = rate
        self.format = audio_format
        self.channels = channels

    def get_content_type_string(self):
        """Returns the content type and params as a string for the websocket
            connection
        """
        return self.content_type + \
            (';layout={}'.format(self.layout) if self.layout else '') + \
            (';rate={}'.format(self.rate) if self.rate else '') + \
            (';format={}'.format(self.format) if self.format else '') + \
            (';channels={}'.format(self.channels) if self.channels else '')
