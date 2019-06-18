import pytest
from src.streaming.streamingclient import RevAiStreamingClient
from src.streaming.MediaConfig import MediaConfig
import threading

@pytest.fixture
def mock_streaming_client(mocker):
    config = MediaConfig()
    streaming_client = RevAiStreamingClient('token', config)
    streaming_client.client.connect = mocker.Mock(name = "mock_connect")
    streaming_client.client.abort = mocker.Mock(name = "mock_abort")
    streaming_client.client.send_binary = mocker.Mock(name = "mock_send_binary")
    streaming_client.client.recv_data = mocker.Mock(name = "mock_recv")
    streaming_client.client.send = mocker.Mock(name = "mock_send")
    return streaming_client

@pytest.fixture
def mock_generator(mocker):
    def gen():
        for i in range(0,3):
            yield i
    return gen