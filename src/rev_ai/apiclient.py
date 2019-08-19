# -*- coding: utf-8 -*-
"""Speech recognition tools for using Rev.ai"""

import requests
import json
import sys
from requests.exceptions import HTTPError
from .models import Job, Account, Transcript, CaptionType
from . import __version__

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class RevAiAPIClient:
    """Client which implements Rev.ai API

    Note that HTTPErrors can be thrown by methods of the API client. The HTTP response payload
    attached to these error is a problem details. The problem details information is represented
    as a JSON object with error specific properties that help to troubleshoot the problem.

    Problem details are defined at https://tools.ietf.org/html/rfc7807.
    """

    # Default version of Rev.ai
    version = 'v1'

    # Default address of the API
    base_url = 'https://api.rev.ai/speechtotext/{}/'.format(version)

    # Rev.ai transcript format
    rev_json_content_type = 'application/vnd.rev.transcript.v1.0+json'

    def __init__(self, access_token):
        """Constructor

        :param access_token: access token which authorizes all requests and links them to your
                             account. Generated on the settings page of your account dashboard
                             on Rev.ai.
        """
        if not access_token:
            raise ValueError('access_token must be provided')

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': 'Bearer {}'.format(access_token),
            'User-Agent': 'RevAi-PythonSDK/{}'.format(__version__)
        })

    def submit_job_url(
            self, media_url,
            metadata=None,
            callback_url=None,
            skip_diarization=False,
            skip_punctuation=False,
            speaker_channel_count=None,
            custom_vocabularies=None):
        """Submit media given a URL for transcription.
        The audio data is downloaded from the URL.

        :param media_url: web location of the media file
        :param metadata: info to associate with the transcription job
        :param callback_url: callback url to invoke on job completion as a webhook
        :param skip_diarization: should rev.ai skip diaization when transcribing this file
        :param skip_punctuation: should rev.ai skip punctuation when transcribing this file
        :param speaker_channel_count: the number of speaker channels in the audio. If provided
            the given audio will have each channel transcribed separately and each channel
            will be treated as a single speaker. [1-8]
        :param custom_vocabularies: a collection of phrase dictionaries. Including custom
            vocabulary will inform and bias the speech recognition to find those phrases.
            Each dictionary should consist of a key "phrases" which maps to a list of strings,
            each of which represents a phrase you would like the speech recognition to bias
            itself toward.
        :returns: raw response data
        :raises: HTTPError
        """
        if not media_url:
            raise ValueError('media_url must be provided')

        payload = {'media_url': media_url}
        if skip_diarization:
            payload['skip_diarization'] = skip_diarization
        if skip_punctuation:
            payload['skip_punctuation'] = skip_punctuation
        if metadata:
            payload['metadata'] = metadata
        if callback_url:
            payload['callback_url'] = callback_url
        if custom_vocabularies:
            payload['custom_vocabularies'] = custom_vocabularies
        if speaker_channel_count:
            payload['speaker_channel_count'] = speaker_channel_count

        response = self._make_http_request(
                       "POST",
                       urljoin(self.base_url, 'jobs'),
                       json=payload
        )

        return Job.from_json(response.json())

    def submit_job_local_file(
            self, filename,
            metadata=None,
            callback_url=None,
            skip_diarization=False,
            skip_punctuation=False,
            speaker_channel_count=None,
            custom_vocabularies=None):
        """Submit a local file for transcription.
        Note that the content type is inferred if not provided.

        :param filename: path to a local file on disk
        :param metadata: info to associate with the transcription job
        :param callback_url: callback url to invoke on job completion as a webhook
        :param skip_diarization: should rev.ai skip diaization when transcribing this file
        :param skip_punctuation: should rev.ai skip punctuation when transcribing this file
        :param speaker_channel_count: the number of speaker channels in the audio. If provided
            the given audio will have each channel transcribed separately and each channel
            will be treated as a single speaker. [1-8]
        :param custom_vocabularies: a collection of phrase dictionaries. Including custom
            vocabulary will inform and bias the speech recognition to find those phrases.
            Each dictionary have the key "phrases" which maps to a list of strings,
            each of which represents a phrase you would like the speech recognition to bias
            itself toward.
        :returns: raw response data
        :raises: HTTPError
        """
        if not filename:
            raise ValueError('filename must be provided')

        payload = {}
        if skip_diarization:
            payload['skip_diarization'] = skip_diarization
        if skip_punctuation:
            payload['skip_punctuation'] = skip_punctuation
        if metadata:
            payload['metadata'] = metadata
        if callback_url:
            payload['callback_url'] = callback_url
        if custom_vocabularies:
            payload['custom_vocabularies'] = custom_vocabularies
        if speaker_channel_count:
            payload['speaker_channel_count'] = speaker_channel_count

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
        :returns: raw response data
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

    def get_captions(self, id_, content_type=CaptionType.SRT):
        """Get the captions output of a specific job and return it as plain text

        :param id_: id of job to be requested
        :param content_type: caption type which should be returned. Defaults to SRT
        :returns: caption data as text
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')
        if sys.version_info > (3, 0):
            content_type = content_type.value

        response = self._make_http_request(
                       "GET",
                       urljoin(self.base_url, 'jobs/{}/captions'.format(id_)),
                       headers={'Accept': str(content_type)}
        )

        return response.text

    def get_captions_as_stream(self, id_, content_type=CaptionType.SRT):
        """Get the captions output of a specific job and return it as a plain text stream

        :param id_: id of job to be requested
        :param content_type: caption type which should be returned. Defaults to SRT
        :returns: requests.models.Response HTTP response which can be used to stream
            the payload of the response
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')
        if sys.version_info > (3, 0):
            content_type = content_type.value

        response = self._make_http_request(
                       "GET",
                       urljoin(self.base_url, 'jobs/{}/captions'.format(id_)),
                       headers={'Accept': str(content_type)},
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
        """Get account information, such as remaining balance.

        :raises: HTTPError
        """
        response = self._make_http_request(
                      "GET",
                      urljoin(self.base_url, 'account')
        )

        return Account.from_json(response.json())

    def _make_http_request(self, method, url, **kwargs):
        """Wrapper method for initiating HTTP requests and handling potential
            errors.

        :param method: string of HTTP method request
        :param url: string containing the URL to make the request to
        :param (optional) **kwargs: potential extra arguments including header
            and stream
        :raises: HTTPError
        """
        response = self.session.request(method, url, **kwargs)

        try:
            response.raise_for_status()
            return response
        except HTTPError as err:
            if (response.content):
                err.args = (err.args[0] +
                            "; Server Response : {}".format(response.content.decode('utf-8')),)
            raise
