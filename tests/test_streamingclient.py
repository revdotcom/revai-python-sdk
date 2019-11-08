# -*- coding: utf-8 -*-
"""Unit tests for the streaming client"""

import pytest
import six
from src.rev_ai import __version__
from src.rev_ai.models.streaming import MediaConfig
from src.rev_ai.streamingclient import RevAiStreamingClient

try:
    from urllib.parse import parse_qs, urlparse
except ImportError:
    from urlparse import parse_qs, urlparse


@pytest.mark.usefixtures('mock_streaming_client', 'mock_generator')
class TestStreamingClient():
    def test_constructor(self):
        example_token = 'token'
        example_config = MediaConfig()
        example_version = 'example_version'
        example_error_func = lambda example_error: example_error
        example_close_func = lambda code, reason: '{}:{}'.format(code, reason)
        example_connect_func = lambda id: id
        example_client = RevAiStreamingClient(
            example_token,
            example_config,
            example_version,
            example_error_func,
            example_close_func,
            example_connect_func
        )

        assert example_client.on_error("Example Error") == 'Example Error'
        assert example_client.on_connected("Example ID") == 'Example ID'
        assert example_client.on_close('1', 'Example Reason') == '1:Example Reason'
        assert example_client.base_url == 'wss://api.rev.ai/speechtotext/example_version/stream'

    def test_constructor_using_defaults(self):
        example_token = 'token'
        example_config = MediaConfig()
        example_client = RevAiStreamingClient(example_token, example_config)

        assert example_client.access_token == 'token'
        assert example_client.config == example_config

    def test_constructor_no_token_no_config(self):
        example_token = 'token'
        example_config = MediaConfig()

        with pytest.raises(ValueError):
            RevAiStreamingClient(example_token, None)
        with pytest.raises(ValueError):
            RevAiStreamingClient(None, example_config)

    def test_start_success(self, mock_streaming_client, mock_generator, capsys):
        custom_vocabulary_id = 'mycustomvocabid'
        metadata = "my metadata"
        query_dict = {
            'access_token': mock_streaming_client.access_token,
            'content_type': mock_streaming_client.config.get_content_type_string(),
            'user_agent': 'RevAi-PythonSDK/{}'.format(__version__),
            'custom_vocabulary_id': custom_vocabulary_id,
            'metadata': metadata
        }
        example_data = '{"type":"partial","transcript":"Test"}'
        example_connected = '{"type":"connected","id":"testid"}'
        if six.PY3:
            example_data = example_data.encode('utf-8')
            example_connected = example_connected.encode('utf-8')
        data = [[0x1, example_connected],
                [0x1, example_data],
                [0x8, b'\x03\xe8End of input. Closing']]
        exp_responses = ['Connected, Job ID : testid\n',
                         '{"type":"partial","transcript":"Test"}',
                         'Connection Closed. Code : 1000; Reason : End of input. Closing\n']
        mock_streaming_client.client.recv_data.side_effect = data

        response_gen = mock_streaming_client.start(mock_generator(), metadata, custom_vocabulary_id)

        assert mock_streaming_client.client.connect.call_count == 1
        called_url = mock_streaming_client.client.connect.call_args_list[0].args[0]
        validate_query_parameters(called_url, query_dict)
        mock_streaming_client.client.send_binary.assert_any_call(0)
        mock_streaming_client.client.send_binary.assert_any_call(1)
        mock_streaming_client.client.send_binary.assert_any_call(2)
        assert hasattr(mock_streaming_client, 'request_thread')
        for ind, response in enumerate(response_gen):
            assert capsys.readouterr().out == exp_responses[ind]
            assert exp_responses[ind + 1] == response
        assert capsys.readouterr().out == exp_responses[2]

    def test_start_failure_to_connect(self, mock_streaming_client, mock_generator):
        mock_streaming_client.client.connect = lambda x: 1 / 0

        with pytest.raises(ZeroDivisionError):
            mock_streaming_client.start(mock_generator())

    def test_end(self, mock_streaming_client):
        mock_streaming_client.end()

        mock_streaming_client.client.abort.assert_called_once_with()


def validate_query_parameters(called_url, query_dict):
    called_query_string = urlparse(called_url).query
    called_query_parameters = parse_qs(called_query_string)
    for key in called_query_parameters:
        assert called_query_parameters[key][0] == query_dict[key]
