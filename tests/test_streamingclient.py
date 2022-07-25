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

    def test_start_noparams_success(self, mock_streaming_client, mock_generator, capsys):
        expected_query_dict = build_expected_query_dict(mock_streaming_client, None, None, None, None, None, None, None,
            None, None, None)

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

        response_gen = mock_streaming_client.start(mock_generator())

        called_url = mock_streaming_client.client.connect.call_args_list[0][0][0]
        validate_query_parameters(called_url, expected_query_dict)
        assert mock_streaming_client.client.connect.call_count == 1
        mock_streaming_client.client.send_binary.assert_any_call(0)
        mock_streaming_client.client.send_binary.assert_any_call(1)
        mock_streaming_client.client.send_binary.assert_any_call(2)
        assert hasattr(mock_streaming_client, 'request_thread')
        for ind, response in enumerate(response_gen):
            assert capsys.readouterr().out == exp_responses[ind]
            assert exp_responses[ind + 1] == response
        assert capsys.readouterr().out == exp_responses[2]

    @pytest.mark.parametrize("metadata", ["my metadata"])
    @pytest.mark.parametrize("custom_vocabulary_id", ["customvocabid"])
    @pytest.mark.parametrize("filter_profanity", [True])
    @pytest.mark.parametrize("remove_disfluencies", [True])
    @pytest.mark.parametrize("delete_after_seconds", [0])
    @pytest.mark.parametrize("detailed_partials", [True])
    @pytest.mark.parametrize("start_ts", [10])
    @pytest.mark.parametrize("transcriber", ["machine"])
    @pytest.mark.parametrize("language", ["en"])
    @pytest.mark.parametrize("skip_postprocessing", [True])
    def test_start_allparams_success(self, mock_streaming_client, mock_generator, capsys,
        metadata, custom_vocabulary_id, filter_profanity, remove_disfluencies, delete_after_seconds,
        detailed_partials, start_ts, transcriber, language, skip_postprocessing):

        expected_query_dict = build_expected_query_dict(
            mock_streaming_client,
            metadata,
            custom_vocabulary_id,
            filter_profanity,
            remove_disfluencies,
            delete_after_seconds,
            detailed_partials,
            start_ts,
            transcriber,
            language,
            skip_postprocessing
        )
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

        response_gen = mock_streaming_client.start(mock_generator(),
            metadata, custom_vocabulary_id, filter_profanity, remove_disfluencies, delete_after_seconds,
            detailed_partials, start_ts, transcriber, language, skip_postprocessing)

        called_url = mock_streaming_client.client.connect.call_args_list[0][0][0]
        validate_query_parameters(called_url, expected_query_dict)
        assert mock_streaming_client.client.connect.call_count == 1
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


def build_expected_query_dict(mock_streaming_client,
    metadata, custom_vocabulary_id, filter_profanity, remove_disfluencies, delete_after_seconds, detailed_partials,
    start_ts, transcriber, language, skip_postprocessing):
    expected_query_dict = {
        'access_token': mock_streaming_client.access_token,
        'content_type': mock_streaming_client.config.get_content_type_string(),
        'user_agent': 'RevAi-PythonSDK/{}'.format(__version__),
    }

    if metadata:
        expected_query_dict["metadata"] = metadata
    if custom_vocabulary_id:
        expected_query_dict["custom_vocabulary_id"] = custom_vocabulary_id
    if filter_profanity:
        expected_query_dict["filter_profanity"] = "true"
    if remove_disfluencies:
        expected_query_dict["remove_disfluencies"] = "true"
    if delete_after_seconds:
        expected_query_dict["delete_after_seconds"] = str(delete_after_seconds)
    if detailed_partials:
        expected_query_dict["detailed_partials"] = "true"
    if start_ts:
        expected_query_dict["start_ts"] = str(start_ts)
    if transcriber:
        expected_query_dict["transcriber"] = transcriber
    if language:
        expected_query_dict["language"] = language
    if skip_postprocessing:
        expected_query_dict["skip_postprocessing"] = "true"

    return expected_query_dict


def validate_query_parameters(called_url, expected_query_dict):
    called_query_string = urlparse(called_url).query
    called_query_parameters = parse_qs(called_query_string)
    for key in expected_query_dict:
        assert called_query_parameters[key][0] == expected_query_dict[key]
