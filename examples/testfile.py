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

from src.rev_ai.models import MediaConfig
from src.rev_ai.streamingclient import RevAiStreamingClient
import os
import json
import io

import pyaudio
from six.moves import queue  
import time
import threading
import _thread
import wave

############### File Example ######################################

#Name of file to be transcribed
filename = "example_file.wav"

#Media configuration of audio file. This includes the content type, rate, format, layout and # of channels
config = MediaConfig("audio/wav")

#Create client with your access token and media configuration
streamclient = RevAiStreamingClient(ACCESS_TOKEN, config)

#Open file and read data into array. Practically, that stream data would be divded into chunks
with io.open(filename, 'rb') as stream:
    data_array = [stream.read()]

#Starts the streaming connection and creates a thread to send bytes from data_array
response_generator = streamclient.start(data_array)

#Iterates through the responses from the server when obtained
for response in response_generator:
    print(response)

#Closes the streaming connection
streamclient.end()

########## Generator Example #########################################

#Creating Media Configuration for the audio. Default lets the server guess based on the audio
config = MediaConfig()

#Creates Streaming Client with a given access token and media configuration
streamclient = RevAiStreamingClient(ACCESS_TOKEN, config)

#Starts the streaming connection with a thread sending the data from the media generator
response_generator = streamclient.start(MEDIA_GENERATOR)

#Iterates through the responses from the server when obtained
for response in response_generator:
    print(response)

#Closes the streaming connection
streamclient.end()
