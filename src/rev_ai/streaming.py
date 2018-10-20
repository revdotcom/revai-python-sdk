"""Basic streaming to Rev's speech recognition API."""
from ws4py.client.threadedclient import WebSocketClient
import json
import threading
import time
import sys


def rate_limited(max_per_second):
    """Decorator to limit the rate client sends data."""
    min_interval = 1.0 / float(max_per_second)

    def decorate(func):
        last_called = [0.0]

        def rate_limited_function(*args, **kargs):
            elapsed = time.clock() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kargs)
            last_called[0] = time.clock()
            return ret
        return rate_limited_function
    return decorate


class RevClient(WebSocketClient):
    """Client for streaming data to the server and receiving the responses."""

    @rate_limited(4)
    def send_data(self, data):
        self.send(data, binary=True)

    def send_file(self, audiofile, byterate):
        """Open and stream a file to the server.

        Creates an additional thread to stream.
        Note: socket is closed once the file is finished.
        """
        def send_data_to_ws():
            with open(audiofile, 'rb') as audiostream:
                block = audiostream.read(byterate // 4)
                while block:
                    self.send_data(block)
                    block = audiostream.read(byterate // 4)
            self.finish_session()
        t = threading.Thread(target=send_data_to_ws)
        t.start()

    def finish_session(self):
        """Close the socket by sending the end-of-sentence signal."""
        self.send("EOS")

    def received_message(self, m):
        """Parse a transcript result."""
        response = json.loads(str(m))
        if response['status'] == 0:
            if 'result' in response:
                trans = response['result']['hypotheses'][0]['transcript']
                if response['result']['final']:
                    print("Final transcript: " + trans)
                else:
                    if len(trans) > 80:
                        trans = "... %s" % trans[-76:]
                    print(trans)


if __name__ == '__main__':
    audiofile = sys.argv[1]
    byterate = 16000 if len(sys.argv) < 3 else int(sys.argv[2])

    # Usage 1
    c = RevClient("ws://localhost:8080/client/ws/speech")
    c.connect()
    with open(audiofile, 'rb') as audiostream:
        block = audiostream.read(byterate // 4)
        while block:
            c.send_data(block)
            block = audiostream.read(byterate // 4)
    c.finish_session()

    # Usage 2
    # c = RevClient("ws://localhost:8080/client/ws/speech")
    # c.connect()
    # c.send_file(audiofile, byterate)
    # time.sleep(20)
