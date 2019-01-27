# -*- coding: utf-8 -*-
"""Speech recognition tools for using Rev.ai"""

import requests
import json
from .models import Job, Account, Transcript

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class RevAiAPIClient:
    """Client which implements Rev.ai API"""

    # Default version of Rev.ai
    version = "v1"

    # Default address of the API
    base_url = "https://api.rev.ai/revspeech/{}/".format(version)

    def __init__(self, api_key):
        """Constructor

        :param api_key: api key which authorizes all requests and links them to
            your account. Generated on the settings page of your account
            dashboard on rev.ai
        """
        if not api_key:
            raise ValueError("api_key must be provided")

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': 'Bearer {}'.format(api_key),
            'User-Agent': 'python_sdk'
        })

    def submit_job_url(
            self, media_url,
            metadata=None,
            callback_url=None,
            skip_diarization=False):
        """Submit media given a URL for transcription.
        The audio data is downloaded from the URL.

        :param media_url: web location of the media file
        :param metadata: info to associate with the transcription job
        :param callback_url: callback url to invoke on job completion as a
                             webhook
        :param skip_diarization: should rev.ai skip diaization when
                                 transcribing this file
        :returns: raw response data
        """
        if not media_url:
            raise ValueError('media_url must be provided')

        url_jobs = urljoin(self.base_url, "jobs")
        payload = {'media_url': media_url}
        if metadata:
            payload['metadata'] = metadata
        if callback_url:
            payload['callback_url'] = callback_url

        response = self.session.post(url_jobs, json=payload)
        response.raise_for_status()

        return Job.from_json(response.json())

    def submit_job_local_file(
            self, filename,
            metadata=None,
            callback_url=None,
            skip_diarization=False):
        """Submit a local file for transcription.
        Note that the content type is inferred if not provided.

        :param filename: path to a local file on disk
        :param metadata: info to associate with the transcription job
        :param callback_url: callback url to invoke on job completion as a
                             webhook
        :param skip_diarization: should rev.ai skip diaization when
                                 transcribing this file
        :returns: raw response data
        """
        if not filename:
            raise ValueError('filename must be provided')

        url_jobs = urljoin(self.base_url, "jobs")
        payload = {}
        if metadata:
            payload['metadata'] = metadata
        if callback_url:
            payload['callback_url'] = callback_url

        with open(filename, 'rb') as f:
            files = {
                'media': (filename, f),
                'options': (None, json.dumps(payload))
            }

            response = self.session.post(url_jobs, files=files)
            response.raise_for_status()

        return Job.from_json(response.json())

    def get_job_details(self, id_):
        """View information about a specific job.
        The server will respond with the status and creation date.

        :param id_: id of the job to be requested
        :returns: raw response data
        """
        if not id_:
            raise ValueError('id_ must be provided')

        url_jobs_id = urljoin(self.base_url, "jobs/{}".format(id_))
        response = self.session.get(url_jobs_id)
        response.raise_for_status()

        return Job.from_json(response.json())

    def get_transcript_text(self, id_):
        """Get the transcript of a specific job as json.

        :param id_: id of job to be requested
        :returns: transcript data as text
        """
        if not id_:
            raise ValueError('id_ must be provided')

        url_jobs_transcript = urljoin(
            self.base_url, "jobs/{}/transcript".format(id_))
        response = self.session.get(
            url_jobs_transcript, headers={'Accept': "text/plain"})
        response.raise_for_status()

        return response.text

    def get_transcript_object(self, id_):
        """Get the transcript of a specific job as json.

        :param id_: id of job to be requested
        :returns: transcript data as a python object
        """
        if not id_:
            raise ValueError('id_ must be provided')

        url_jobs_transcript = urljoin(
            self.base_url, "jobs/{}/transcript".format(id_))
        response = self.session.get(
            url_jobs_transcript,
            headers={'Accept': 'application/{}+json'
                     .format("vnd.rev.transcript.v1.0")})
        response.raise_for_status()

        return Transcript.from_json(response.json())

    def get_account(self):
        """Get account information, such as remaining balance.
        """
        url_account = urljoin(self.base_url, "account")
        response = self.session.get(url_account)
        response.raise_for_status()

        return Account.from_json(response.json())
