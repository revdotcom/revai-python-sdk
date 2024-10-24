# Rev AI Python SDK

[![CI](https://github.com/revdotcom/revai-python-sdk/actions/workflows/build_test.yml/badge.svg)](https://github.com/revdotcom/revai-python-sdk/actions/workflows/build_test.yml)

## Documentation

See the [API docs](https://docs.rev.ai/sdk/python/) for more information about the API and
more python examples.

## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

    pip install --upgrade rev_ai

Install from source with:

    python setup.py install

### Requirements

- Python 3.8+

## Usage

All you need to get started is your Access Token, which can be generated on
your [AccessToken Settings Page](https://www.rev.ai/access_token). Create a client with the
generated Access Token:

```python
from rev_ai import apiclient, RevAiApiDeploymentConfigMap, RevAiApiDeployment

# create your client
# optionally configure the Rev AI deployment to use
client = apiclient.RevAiAPIClient("ACCESS TOKEN", url=RevAiApiDeploymentConfigMap[RevAiApiDeployment.US]['base_url'])
```

### Sending a file

Once you've set up your client with your Access Token sending a file is easy!

```python
# you can send a local file
job = client.submit_job_local_file("FILE PATH")

# or send a link to the file you want transcribed
job = client.submit_job_url("https://example.com/file-to-transcribe.mp3")
```

`job` will contain all the information normally found in a successful response from our
[Submit Job](https://docs.rev.ai/api/asynchronous/reference/#operation/SubmitTranscriptionJob) endpoint.

If you want to get fancy, both submit job methods take `metadata`,`notification_config`, 
`skip_diarization`, `skip_punctuation`, `speaker_channels_count`,`custom_vocabularies`,
`filter_profanity`, `remove_disfluencies`, `delete_after_seconds`,`language`,
and `custom_vocabulary_id` as optional parameters.

The url submission option also supports authentication headers by using the `source_config` option.

You can request transcript summary.

```python
# submitting a human transcription jobs
job = client.submit_job_url("https://example.com/file-to-transcribe.mp3",
    language='en',
    summarization_config=SummarizationOptions(
        formatting_type=SummarizationFormattingOptions.BULLETS
    ))
```

You can request transcript translation into up to five languages.

```javascript
job = client.submit_job_url("https://example.com/file-to-transcribe.mp3",
    language='en',
    translation_config=TranslationOptions(
        target_languages: [
            TranslationLanguageOptions("es", TranslationModel.PREMIUM),
            TranslationLanguageOptions("de")
        ]
    ));
```

All options are described in the request body of the
[Submit Job](https://docs.rev.ai/api/asynchronous/reference/#operation/SubmitTranscriptionJob) endpoint.

### Human Transcription

If you want transcription to be performed by a human, both methods allow you to submit human transcription jobs
using `transcriber=human` with `verbatim`, `rush`, `segments_to_transcribe` and `test_mode` as optional parameters.
Check out our documentation for [Human Transcription](https://docs.rev.ai/api/asynchronous/transcribers/#human-transcription) for more details.

```python
# submitting a human transcription jobs
job = client.submit_job_url("https://example.com/file-to-transcribe.mp3",
    transcriber='human',
    verbatim=False,
    rush=False,
    test_mode=True
    segments_to_transcribe=[{
        start: 2.0,
        end: 4.5
    }])
```

### Checking your file's status

You can check the status of your transcription job using its `id`

```python
job_details = client.get_job_details(job.id)
```

`job_details` will contain all information normally found in a successful response from
our [Get Job](https://docs.rev.ai/api/asynchronous/reference/#operation/GetJobById) endpoint

### Checking multiple files

You can retrieve a list of transcription jobs with optional parameters

```python
jobs = client.get_list_of_jobs()

# limit amount of retrieved jobs
jobs = client.get_list_of_jobs(limits=3)

# get jobs starting after a certain job id
jobs = client.get_list_of_jobs(starting_after='Umx5c6F7pH7r')
```

`jobs` will contain a list of job details having all information normally found in a successful response
from our [Get List of Jobs](https://docs.rev.ai/api/asynchronous/reference/#operation/GetListOfJobs) endpoint

### Deleting a job

You can delete a transcription job using its `id`

```python
client.delete_job(job.id)
```

 All data related to the job, such as input media and transcript, will be permanently deleted.
 A job can only by deleted once it's completed (either with success or failure).

### Getting your transcript

Once your file is transcribed, you can get your transcript in a few different forms:

```python
# as text
transcript_text = client.get_transcript_text(job.id)

# as json
transcript_json = client.get_transcript_json(job.id)

# or as a python object
transcript_object = client.get_transcript_object(job.id)

# or if you requested transcript translation(s)
transcript_object = client.get_translated_transcript_object(job.id,'es')
```

Both the json and object forms contain all the formation outlined in the response
of the [Get Transcript](https://docs.rev.ai/api/asynchronous/reference/#operation/GetTranscriptById) endpoint
when using the json response schema. While the text output is a string containing
just the text of your transcript

### Getting transcript summary

If you requested transcript summary, you can retrieve it as plain text or structured object:

```python
# as text
summary = client.get_transcript_summary_text(job.id)

# as json
summary = client.get_transcript_summary_json(job.id)

# or as a python object
summary = client.get_transcript_summary_object(job.id)

```
### Getting captions output

You can also get captions output from the SDK. We offer both SRT and VTT caption formats.
If you submitted your job as speaker channel audio then you must also provide a `channel_id` to be captioned:

```python
captions = client.get_captions(job.id, content_type=CaptionType.SRT, channel_id=None)

# or if you requested transcript translation(s)
captions = client.get_translated_captions(job.id, 'es')

```

### Streamed outputs

Any output format can be retrieved as a stream. In these cases we return the raw http response to you. The output can be retrieved via `response.content`, `response.iter_lines()` or `response.iter_content()`.

```python
text_stream = client.get_transcript_text_as_stream(job.id)

json_stream = client.get_transcript_json_as_stream(job.id)

captions_stream = client.get_captions_as_stream(job.id)
```

## Streaming audio

In order to stream audio, you will need to setup a streaming client and a media configuration for the audio you will be sending.

```python
from rev_ai.streamingclient import RevAiStreamingClient
from rev_ai.models import MediaConfig, RevAiApiDeploymentConfigMap, RevAiApiDeployment

#on_error(error)
#on_close(code, reason)
#on_connected(id)

# optionally configure the Rev AI deployment to use
config = MediaConfig()
streaming_client = RevAiStreamingClient("ACCESS TOKEN",
                                        config,
                                        on_error=ERRORFUNC,
                                        on_close=CLOSEFUNC,
                                        on_connected=CONNECTEDFUNC,
                                        url=RevAiApiDeploymentConfigMap[RevAiApiDeployment.US]['base_websocket_url'])
```

`on_error`, `on_close`, and `on_connected` are optional parameters that are functions to be called when the websocket errors, closes, and connects respectively. The default `on_error` raises the error, `on_close` prints out the code and reason for closing, and `on_connected` prints out the job ID.
If passing in custom functions, make sure you provide the right parameters. See the sample code for the parameters.

Once you have a streaming client setup with a `MediaConfig` and access token, you can obtain a transcription generator of your audio. You can also use a custom vocabulary with your streaming job by supplying the optional `custom_vocabulary_id` when starting a connection!

More optional parameters can be supplied when starting a connection, these are `metadata`, `filter_profanity`, `remove_disfluencies`, `delete_after_seconds`, and `detailed_partials`. For a description of these optional parameters look at our [streaming documentation](https://docs.rev.ai/api/streaming/requests/#request-parameters).

```python
response_generator = streaming_client.start(AUDIO_GENERATOR, custom_vocabulary_id="CUSTOM VOCAB ID")
```

`response_generator` is a generator object that yields the transcription results of the audio including partial and final transcriptions. The `start` method creates a thread sending audio pieces from the `AUDIO_GENERATOR` to our
[streaming] endpoint.

If you want to end the connection early, you can!

```python
streaming_client.end()
```

Otherwise, the connection will end when the server obtains an "EOS" message.

### Submitting custom vocabularies

In addition to passing custom vocabularies as parameters in the async API client, you can create and submit your custom vocabularies independently and directly to the custom vocabularies API, as well as check on their progress.

Primarily, the custom vocabularies client allows you to submit and preprocess vocabularies for use with the streaming client, in order to have streaming jobs with custom vocabularies!

In this example you see how to construct custom vocabulary objects, submit them to the API, and check on their progress and metadata!

```python
from rev_ai import custom_vocabularies_client
from rev_ai.models import CustomVocabulary

# Create a client
client = custom_vocabularies_client.RevAiCustomVocabulariesClient("ACCESS TOKEN")

# Construct a CustomVocabulary object using your desired phrases
custom_vocabulary = CustomVocabulary(["Patrick Henry Winston", "Robert C Berwick", "Noam Chomsky"])

# Submit the CustomVocabulary
custom_vocabularies_job = client.submit_custom_vocabularies([custom_vocabulary])

# View the job's progress
job_state = client.get_custom_vocabularies_information(custom_vocabularies_job['id'])

# Get list of previously submitted custom vocabularies
custom_vocabularies_jobs = client.get_list_of_custom_vocabularies()

# Delete the CustomVocabulary
client.delete_custom_vocabulary(custom_vocabularies_job['id'])
```

For more details, check out the custom vocabularies example in our [examples](https://github.com/revdotcom/revai-python-sdk/tree/develop/examples).

# For Rev AI Python SDK Developers

Remember in your development to follow the PEP8 style guide. Your code editor likely has Python PEP8 linting packages which can assist you in your development.

# Local testing instructions

Prequisites: virtualenv, tox

To test locally use the following commands from the repo root

    virtualenv ./sdk-test
    . ./sdk-test/bin/activate
    tox

This will locally run the test suite, and saves significant dev time over
waiting for the CI tool to pick it up.
