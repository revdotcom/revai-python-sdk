# -*- coding: utf-8 -*-
"""Unit tests for the media config class"""

from src.rev_ai.models.streaming import MediaConfig


class TestMediaConfig():
    def test_constructor(self):
        example_config = MediaConfig('content_type',
                                     'layout',
                                     'rate',
                                     'format',
                                     'channels')

        assert example_config.content_type == 'content_type'
        assert example_config.layout == 'layout'
        assert example_config.rate == 'rate'
        assert example_config.format == 'format'
        assert example_config.channels == 'channels'

    def test_constructor_with_defaults(self):
        example_config = MediaConfig()

        assert example_config.content_type == 'audio/*'
        assert not example_config.layout
        assert not example_config.rate
        assert not example_config.format
        assert not example_config.channels

    def test_get_content_type_string_all(self):
        example_config = MediaConfig('content_type',
                                     'LAYOUT',
                                     'RATE',
                                     'FORMAT',
                                     'CHANNELS')

        content_type_string = example_config.get_content_type_string()

        assert content_type_string == ('content_type'
                                       ';layout=LAYOUT'
                                       ';rate=RATE'
                                       ';format=FORMAT'
                                       ';channels=CHANNELS')

    def test_get_content_type_string_missing(self):
        example_config = MediaConfig('content_type',
                                     '',
                                     '',
                                     '',
                                     'CHANNELS')

        content_type_string = example_config.get_content_type_string()

        assert content_type_string == 'content_type;channels=CHANNELS'
