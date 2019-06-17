"""StreamingClient tool used for streaming services"""
from AudioConfig import AudioConfig
import websocket
import io
import threading
import six
import json

def on_error(error):
    raise error

def on_close(code, reason):
    print("{} : {}".format(code, reason))

def on_connected(job_id):
    print('Connected, Job ID : {}'.format(job_id))

class RevAiStreamingClient():
    def __init__(self, 
                access_token, 
                config, 
                version = 'v1alpha',  
                on_error = on_error, 
                on_close = on_close, 
                on_connected = on_connected):
        """Constructor for Streaming Client

        :param access_token: access token which authorizes all requests and links them to your
                             account. Generated on the settings page of your account dashboard
                             on Rev.ai.
        :param config: an AudioConfig object containing audio information. 
                       See AudioConfig.py for more information
        :param version (optional): version of the streaming speech to text as string
        :param on_message (optional): function to be called when recieving a message from the server
        :param on_error (optional): function to be called when recieving an error from the server
        :param on_close (optional): function to be called when the websocket closes
        :param on_connected (optional): function to be called when the websocket and thread starts successfully
        """
        if not access_token:
            raise ValueError('access_token must be provided')

        if not config:
            raise ValueError('config must be provided')

        self.access_token = access_token
        self.config = config
        self.base_url = base_url = 'wss://api.rev.ai/speechtotext/{}/stream'.format(version)
        self.on_error = on_error
        self.on_close = on_close
        self.on_connected = on_connected
        self.client = websocket.WebSocket(enable_multithread = True, 
            on_error = self.on_error, 
            on_close = self.on_close, 
            on_connected = self.on_connected)

    def start(self, generator):
        """Function to connect thde websocket to the URL and start the response thread

        :param generator: generator object that yields binary audio data
        """
        url = self.base_url + '?access_token={}'.format(self.access_token) \
             + '&content_type={}'.format(self.config.get_content_type_string())
        try:
            self.client.connect(url)
            self._start_send_data_thread(generator)
            return self._responses()
        except Exception as e:
            self.client.abort()
            self.on_error(e)

    def end(self):
        """Function to end the streaming service, close the websocket.
        """
        self.client.abort()

    def _start_send_data_thread(self, generator):
        """Function to send binary audio data from a generator with threading

        :param generator: generator object that yields binary audio data
        """
        if not generator:
            raise ValueError('generator must be provided')

        if hasattr(self, 'request_thread'):
            if self.request_thread.isAlive():
                raise ValueError("""Data is still being sent and will interfere with the responses.""")

        self.request_thread = threading.Thread(target = self._send_data, 
                                args = [generator])
        self.request_thread.start()

    def _send_data(self, generator):
        """Function used in a thread to send requests to the server.

        :param generator: enerator object that yields binary audio data
        """
        if not generator:
            raise ValueError('generator must be provided')

        for chunk in generator:
            self.client.send_binary(chunk)

        self.client.send("EOS")

    def _responses(self):
        """A generator of reponses from the server. Yields the data decoded.
        """
        while True:
            with self.client.readlock:
                opcode, data = self.client.recv_data()
            if six.PY3 and opcode == websocket.ABNF.OPCODE_TEXT:
                dec_data = data.decode('utf-8') 
                data_dict = json.loads(dec_data)
                if data_dict['type'] == 'connected':
                    yield self.on_connected(data_dict['id'])
                else:
                    yield dec_data
            elif opcode == websocket.ABNF.OPCODE_TEXT:
                data_dict = json.loads(dec_data)
                if data_dict['type'] == 'connected':
                    yield self.on_connected(data_dict['id'])
                else:
                    yield data
            elif opcode == websocket.ABNF.OPCODE_CLOSE:
                if data and len(data) >= 2:
                    code = 256 * six.byte2int(data[0:1]) + \
                            six.byte2int(data[1:2])
                    reason = data[2:].decode('utf-8')
                    self.on_close(code, reason)
                return
            else:
                yield ''