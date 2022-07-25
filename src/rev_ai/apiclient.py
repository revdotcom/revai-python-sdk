# -*- coding: utf-8 -*-
"""Speech recognition tools for using Rev AI"""

import json
from .models import Account, CaptionType, Job, Transcript
from .baseclient import BaseClient
from . import utils

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class RevAiAPIClient(BaseClient):
    """Client which implements Rev AI API

    Note that HTTPErrors can be thrown by methods of the API client. The HTTP
    response payload attached to these error is a problem details. The problem
    details information is represented as a JSON object with error specific
    properties that help to troubleshoot the problem.

    Problem details are defined at https://tools.ietf.org/html/rfc7807.
    """

    # Default version of Rev AI
    version = 'v1'

    # Default base url for Rev AI
    base_url = 'https://api.rev.ai/speechtotext/{}/'.format(version)

    # Rev AI transcript format
    rev_json_content_type = 'application/vnd.rev.transcript.v1.0+json'

    def __init__(self, access_token):
        """Constructor

        :param access_token: access token which authorizes all requests and links them to your
                             account. Generated on the settings page of your account dashboard
                             on Rev AI.
        """

        BaseClient.__init__(self, access_token)

    def submit_job_url(
            self,
            media_url=None,
            metadata=None,
            callback_url=None,
            skip_diarization=False,
            skip_punctuation=False,
            speaker_channels_count=None,
            custom_vocabularies=None,
            filter_profanity=False,
            remove_disfluencies=False,
            delete_after_seconds=None,
            language=None,
            custom_vocabulary_id=None,
            transcriber=None,
            verbatim=None,
            rush=None,
            test_mode=None,
            segments_to_transcribe=None,
            speaker_names=None,
            source_config=None,
            notification_config=None,
            skip_postprocessing=False):
        """Submit media given a URL for transcription.
        The audio data is downloaded from the URL
        :param media_url: web location of the media file
        .. deprecated:: 2.16.0
            Use source_config instead
        :param metadata: info to associate with the transcription job
        :param callback_url: callback url to invoke on job completion as a webhook
        .. deprecated:: 2.16.0
            Use notification_config instead
        :param skip_diarization: should Rev AI skip diarization when transcribing this file
        :param skip_punctuation: should Rev AI skip punctuation when transcribing this file
        :param speaker_channels_count: the number of speaker channels in the
            audio. If provided the given audio will have each channel
            transcribed separately and each channel will be treated as a single
            speaker. Valid values are integers 1-8 inclusive.
        :param custom_vocabularies: a collection of phrase dictionaries.
            Including custom vocabulary will inform and bias the speech
            recognition to find those phrases. Each dictionary should consist
            of a key "phrases" which maps to a list of strings, each of which
            represents a phrase you would like the speech recognition to bias
            itself toward. Cannot be used with the custom_vocabulary_id parameter.
        :param filter_profanity: whether to mask profane words
        :param remove_disfluencies: whether to exclude filler words like "uh"
        :param delete_after_seconds: number of seconds after job completion when job is auto-deleted
        :param language: specify language using the one of the supported ISO 639-1 (2-letter) or
            ISO 639-3 (3-letter) language codes as defined in the API Reference
        :param custom_vocabulary_id: The id of a pre-completed custom vocabulary
            submitted through the custom vocabularies api. Cannot be used with the
            custom_vocabularies parameter.
        :param transcriber: type of transcriber to use to transcribe the media file
        :param verbatim: Only available with "human" transcriber.
            Whether human transcriber transcribes every syllable.
        :param rush: Only available with "human" transcriber.
            Whether job is given higher priority to be worked on sooner for higher pricing.
        :param test_mode: Only available with "human" transcriber.
            Whether human transcription job is mocked and no transcription actually happens.
        :param segments_to_transcribe: Only available with "human" transcriber.
            Sections of transcript needed to be transcribed.
        :param speaker_names: Only available with "human" transcriber.
            Human readable names of speakers in the file.
        :param source_config: CustomerUrlData object containing url of the source media and
            optional authentication headers to use when accessing the source url
        :param notification_config: CustomerUrlData object containing the callback url to
            invoke on job completion as a webhook and optional authentication headers to use when
            calling the callback url
        :param skip_postprocessing: skip all text postprocessing (punctuation, capitalization, ITN)
        :returns: raw response data
        :raises: HTTPError
        """
        payload = self._create_job_options_payload(media_url, metadata, callback_url,
                                                   skip_diarization, skip_punctuation,
                                                   speaker_channels_count,
                                                   custom_vocabularies, filter_profanity,
                                                   remove_disfluencies, delete_after_seconds,
                                                   language, custom_vocabulary_id, transcriber,
                                                   verbatim, rush, test_mode,
                                                   segments_to_transcribe, speaker_names,
                                                   source_config, notification_config,
                                                   skip_postprocessing)

        response = self._make_http_request(
            "POST",
            urljoin(self.base_url, 'jobs'),
            json=payload
        )

        return Job.from_json(response.json())

    def submit_job_local_file(
            self,
            filename,
            metadata=None,
            callback_url=None,
            skip_diarization=False,
            skip_punctuation=False,
            speaker_channels_count=None,
            custom_vocabularies=None,
            filter_profanity=False,
            remove_disfluencies=False,
            delete_after_seconds=None,
            language=None,
            custom_vocabulary_id=None,
            transcriber=None,
            verbatim=None,
            rush=None,
            test_mode=None,
            segments_to_transcribe=None,
            speaker_names=None,
            notification_config=None,
            skip_postprocessing=False):
        """Submit a local file for transcription.
        Note that the content type is inferred if not provided.

        :param filename: path to a local file on disk
        :param metadata: info to associate with the transcription job
        :param callback_url: callback url to invoke on job completion as a webhook
        .. deprecated:: 2.16.0
                Use notification_config instead
        :param skip_diarization: should Rev AI skip diarization when transcribing this file
        :param skip_punctuation: should Rev AI skip punctuation when transcribing this file
        :param speaker_channels_count: the number of speaker channels in the
            audio. If provided the given audio will have each channel
            transcribed separately and each channel will be treated as a single
            speaker. Valid values are integers 1-8 inclusive.
        :param custom_vocabularies: a collection of phrase dictionaries.
            Including custom vocabulary will inform and bias the speech
            recognition to find those phrases. Each dictionary has the key
            "phrases" which maps to a list of strings, each of which represents
            a phrase you would like the speech recognition to bias itself toward.
            Cannot be used with the custom_vocabulary_id parameter
        :param filter_profanity: whether to mask profane words
        :param remove_disfluencies: whether to exclude filler words like "uh"
        :param delete_after_seconds: number of seconds after job completion when job is auto-deleted
        :param language: specify language using the one of the supported ISO 639-1 (2-letter) or
            ISO 639-3 (3-letter) language codes as defined in the API Reference
        :param custom_vocabulary_id: The id of a pre-completed custom vocabulary
            submitted through the custom vocabularies api. Cannot be used with the
            custom_vocabularies parameter.
        :param transcriber: type of transcriber to use to transcribe the media file
        :param verbatim: Only available with "human" transcriber.
            Whether human transcriber transcribes every syllable.
        :param rush: Only available with "human" transcriber.
            Whether job is given higher priority to be worked on sooner for higher pricing.
        :param test_mode: Only available with "human" transcriber.
            Whether human transcription job is mocked and no transcription actually happens.
        :param segments_to_transcribe: Only available with "human" transcriber.
            Sections of transcript needed to be transcribed.
        :param speaker_names: Only available with "human" transcriber.
            Human readable names of speakers in the file.
        :param notification_config: CustomerUrlData object containing the callback url to
            invoke on job completion as a webhook and optional authentication headers to use when
            calling the callback url
        :param skip_postprocessing: skip all text postprocessing (punctuation, capitalization, ITN)
        :returns: raw response data
        :raises: HTTPError, ValueError
        """
        if not filename:
            raise ValueError('filename must be provided')

        payload = self._create_job_options_payload(None, metadata, callback_url,
                                                   skip_diarization, skip_punctuation,
                                                   speaker_channels_count,
                                                   custom_vocabularies, filter_profanity,
                                                   remove_disfluencies, delete_after_seconds,
                                                   language, custom_vocabulary_id, transcriber,
                                                   verbatim, rush, test_mode,
                                                   segments_to_transcribe, speaker_names, None,
                                                   notification_config, skip_postprocessing)

        with open(filename, 'rb') as f:
            files = {
                'media': (filename, f),
                'options': (None, json.dumps(payload, sort_keys=True))
            }

            response = self._make_http_request(
                "POST",
                urljoin(self.base_url, 'jobs'),
                files=files
            )

        return Job.from_json(response.json())

    def get_job_details(self, id_):
        """View information about a specific job.
        The server will respond with the status and creation date.

        :param id_: id of the job to be requested
        :returns: Job object if available
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')

        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, 'jobs/{}'.format(id_))
        )

        return Job.from_json(response.json())

    def get_list_of_jobs(self, limit=None, starting_after=None):
        """Get a list of transcription jobs submitted within the last week in reverse
        chronological order up to the provided limit number of jobs per call.
        Pagination is supported via passing the last job id from previous call into starting_after.

        :param limit: optional, limits the number of jobs returned,
                      if none, a default of 100 jobs is returned, max limit if 1000
        :param starting_after: optional, returns jobs created after the job with this id,
                               exclusive (job with this id is not included)
        :returns: list of jobs response data
        :raises: HTTPError
        """
        params = []
        if limit is not None:
            params.append('limit={}'.format(limit))
        if starting_after is not None:
            params.append('starting_after={}'.format(starting_after))

        query = '?{}'.format('&'.join(params))
        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, 'jobs{}'.format(query))
        )

        return [Job.from_json(job) for job in response.json()]

    def get_transcript_text(self, id_):
        """Get the transcript of a specific job as plain text.

        :param id_: id of job to be requested
        :returns: transcript data as text
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')

        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, 'jobs/{}/transcript'.format(id_)),
            headers={'Accept': 'text/plain'}
        )

        return response.text

    def get_transcript_text_as_stream(self, id_):
        """Get the transcript of a specific job as a plain text stream.

        :param id_: id of job to be requested
        :returns: requests.models.Response HTTP response which can be used to stream
            the payload of the response
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')

        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, 'jobs/{}/transcript'.format(id_)),
            headers={'Accept': 'text/plain'},
            stream=True
        )

        return response

    def get_transcript_json(self, id_):
        """Get the transcript of a specific job as json.

        :param id_: id of job to be requested
        :returns: transcript data as json
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')

        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, 'jobs/{}/transcript'.format(id_)),
            headers={'Accept': self.rev_json_content_type}
        )

        return response.json()

    def get_transcript_json_as_stream(self, id_):
        """Get the transcript of a specific job as streamed json.

        :param id_: id of job to be requested
        :returns: requests.models.Response HTTP response which can be used to stream
            the payload of the response
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')

        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, 'jobs/{}/transcript'.format(id_)),
            headers={'Accept': self.rev_json_content_type},
            stream=True
        )

        return response

    def get_transcript_object(self, id_):
        """Get the transcript of a specific job as a python object`.

        :param id_: id of job to be requested
        :returns: transcript data as a python object
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')

        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, 'jobs/{}/transcript'.format(id_)),
            headers={'Accept': self.rev_json_content_type}
        )

        return Transcript.from_json(response.json())

    def get_captions(self, id_, content_type=CaptionType.SRT, channel_id=None):
        """Get the captions output of a specific job and return it as plain text

        :param id_: id of job to be requested
        :param content_type: caption type which should be returned. Defaults to SRT
        :param channel_id: id of speaker channel to be captioned, only matters for multichannel jobs
        :returns: caption data as text
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')
        query = self._create_captions_query(channel_id)

        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, 'jobs/{0}/captions{1}'.format(id_, query)),
            headers={'Accept': content_type.value}
        )

        return response.text

    def get_captions_as_stream(self, id_, content_type=CaptionType.SRT, channel_id=None):
        """Get the captions output of a specific job and return it as a plain text stream

        :param id_: id of job to be requested
        :param content_type: caption type which should be returned. Defaults to SRT
        :param channel_id: id of speaker channel to be captioned, only matters for multichannel jobs
        :returns: requests.models.Response HTTP response which can be used to stream
            the payload of the response
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')
        query = self._create_captions_query(channel_id)

        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, 'jobs/{0}/captions{1}'.format(id_, query)),
            headers={'Accept': content_type.value},
            stream=True
        )

        return response

    def delete_job(self, id_):
        """Delete a specific transcription job
        All data related to the job, such as input media and transcript, will be permanently
        deleted. A job can only by deleted once it's completed.

        :param id_: id of job to be deleted
        :returns: None if job was successfully deleted
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')

        self._make_http_request(
            "DELETE",
            urljoin(self.base_url, 'jobs/{}'.format(id_)),
        )

        return

    def get_account(self):
        """Get account information, such as remaining credits.

        :raises: HTTPError
        """
        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, 'account')
        )

        return Account.from_json(response.json())

    def _create_job_options_payload(
            self,
            media_url=None,
            metadata=None,
            callback_url=None,
            skip_diarization=None,
            skip_punctuation=None,
            speaker_channels_count=None,
            custom_vocabularies=None,
            filter_profanity=None,
            remove_disfluencies=None,
            delete_after_seconds=None,
            language=None,
            custom_vocabulary_id=None,
            transcriber=None,
            verbatim=None,
            rush=None,
            test_mode=None,
            segments_to_transcribe=None,
            speaker_names=None,
            source_config=None,
            notification_config=None,
            skip_postprocessing=False):
        payload = {}
        if media_url:
            payload['media_url'] = media_url
        if skip_diarization:
            payload['skip_diarization'] = skip_diarization
        if skip_punctuation:
            payload['skip_punctuation'] = skip_punctuation
        if metadata:
            payload['metadata'] = metadata
        if callback_url:
            payload['callback_url'] = callback_url
        if custom_vocabularies:
            payload['custom_vocabularies'] = utils._process_vocabularies(custom_vocabularies)
        if speaker_channels_count:
            payload['speaker_channels_count'] = speaker_channels_count
        if filter_profanity:
            payload['filter_profanity'] = filter_profanity
        if remove_disfluencies:
            payload['remove_disfluencies'] = remove_disfluencies
        if delete_after_seconds is not None:
            payload['delete_after_seconds'] = delete_after_seconds
        if language:
            payload['language'] = language
        if custom_vocabulary_id:
            payload['custom_vocabulary_id'] = custom_vocabulary_id
        if transcriber:
            payload['transcriber'] = transcriber
        if verbatim:
            payload['verbatim'] = verbatim
        if rush:
            payload['rush'] = rush
        if test_mode:
            payload['test_mode'] = test_mode
        if segments_to_transcribe:
            payload['segments_to_transcribe'] = segments_to_transcribe
        if speaker_names:
            payload['speaker_names'] =\
                utils._process_speaker_names(speaker_names)
        if source_config:
            payload['source_config'] = source_config.to_dict()
        if notification_config:
            payload['notification_config'] = notification_config.to_dict()
        if skip_postprocessing:
            payload['skip_postprocessing'] = skip_postprocessing
        return payload

    def _create_captions_query(self, speaker_channel):
        return '' if speaker_channel is None else '?speaker_channel={}'.format(speaker_channel)
