"""Copyright 2019 REV
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from rev_ai.models import MediaConfig
from rev_ai.streamingclient import RevAiStreamingClient
import io


# Name of file to be transcribed
filename = "english_test.raw"

# String of your access token
access_token = "your_access_token"

# Media configuration of audio file.
# This includes the content type, layout, rate, format, and # of channels
config = MediaConfig("audio/x-raw", "interleaved", 16000, "S16LE", 1)

# Create client with your access token and media configuration
streamclient = RevAiStreamingClient(access_token, config)

# Open file and read data into array.
# Practically, stream data would be divided into chunks
with io.open(filename, 'rb') as stream:
    MEDIA_GENERATOR = [stream.read()]

# Starts the streaming connection and creates a thread to send bytes from the
# MEDIA_GENERATOR. response_generator is a generator yielding responses from
# the server
response_generator = streamclient.start(MEDIA_GENERATOR)

# Iterates through the responses from the server when obtained
for response in response_generator:
    print(response)

# Ends the connection early. Not needed as the server will close the connection
# upon receiving an "EOS" message.
streamclient.end()