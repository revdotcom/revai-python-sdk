"""StreamingClient tool used for streaming services"""
from AudioConfig import AudioConfig
import websocket
import io
import threading
import six
import json

def on_error(error):
    pass

def on_close(code, reason):
    pass

def on_open():
    pass

class RevAiStreamingClient():
    def __init__(self, 
                access_token, 
                config, 
                version = 'v1alpha',  
                on_error = on_error, 
                on_close = on_close, 
                on_open = on_open):
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
        :param on_open (optional): function to be called when the websocket and thread starts successfully
        """
        if not access_token:
            raise ValueError('access_token must be provided')

        if not config:
            raise ValueError('config must be provided')


        self.access_token = access_token
        self.config = config
        self.base_url = \
                'wss://api.rev.ai/speechtotext/{}/stream'.format(version)
        self.on_error = on_error
        self.on_close = on_close
        self.on_open = on_open
        self.thread = SpeechThread
        self.client = websocket.WebSocket(enable_multithread = True, 
            on_error = self.on_error, 
            on_close = self.on_close, 
            on_open = self.on_open
            )

    def start(self):
        """Function to connect the websocket to the URL and start the response thread
        """
        url = self.base_url + '?access_token={}'.format(self.access_token) \
              + '&content_type={}'.format(self.config.get_content_type_string()
                )
        try:
            self.client.connect(url)
            self.on_open()
        except Exception as e:
            self.client.abort()
            self.on_error(e)

    def end(self):
        """Function to end the streaming service, close the websocket.
        """
        self.client.abort()

    def send_data_as_gen(self, generator):
        """Function to send binary audio data from a generator

        :param generator: generator object that yields binary audio data
        """
        if not generator:
            raise ValueError('generator must be provided')

        if hasattr(self, 'request_thread'):
            if self.request_thread.isAlive():
                raise ValueError("""Data is still being sent and will interfere 
                    with the responses.""")

        self.request_thread = self.thread(self.RequestSending, [generator])
        self.request_thread.start()

    def send_data_as_filepath(self, filepath):
        """Function to send audio data from a given file

        :param filepath: string containing file location
        """
        if not filepath:
            raise ValueError('filepath must be provided')

        if hasattr(self, 'request_thread'):
            if self.request_thread.isAlive():
                raise ValueError("""Data is still being sent and will interfere 
                    with the responses.""")

        self.send_data_as_gen(self.make_gen(filepath))

    def make_gen(self, filepath):
        """Get generator of audio data from a given filepath
        
        :param filepath: path to file including file name as string
        :returns: generator of audio bytes
        """
        if not filepath:
            raise ValueError('filepath must be provided')

        with io.open(filepath, 'rb') as stream:
            while True:
                piece = stream.read(8192)
                if not piece:
                    break
                yield piece

    def RequestSending(self, generator):
        """Function used in a thread to send requests to the server.

        :param generator: generator object yielding audio data
        """
        if not generator:
            raise ValueError('generator must be provided')

        for chunk in generator:
            self.client.send_binary(chunk)

        self.client.send("EOS")

    def responses(self):
        """A generator of reponses from the server. Yields the data decoded.
        """
        while True:
            with self.client.readlock:
                opcode, response = self.client.recv_data()
            if six.PY3 and opcode == websocket.ABNF.OPCODE_TEXT:
                yield response.decode("utf-8")
            elif opcode == websocket.ABNF.OPCODE_TEXT:
                yield response
            elif opcode == websocket.ABNF.OPCODE_CLOSE:
                if response and len(response) >= 2:
                    code = 256 * six.byte2int(response[0:1]) + six.byte2int(response[1:2])
                    reason = response[2:].decode('utf-8')
                    self.on_close(code, reason)
                return
            else:
                yield ''

class SpeechThread(threading.Thread):
    def __init__(self, function, arg = None):
        """Constructor for Speech Thread Class

        :param function: function to be called by the thread
        :param arg (optional): tuple of optional arguments to pass to the function
        """
        if not function:
            raise ValueError('function must be provided')

        threading.Thread.__init__(self)
        self.function = function
        self.arg = arg

    def run(self):
        """Function that to get called by thread.start(). Simply calls the function
           with arguments passed in the constructor.
        """
        if self.arg:
            self.function(*self.arg)
        else:
            self.function()