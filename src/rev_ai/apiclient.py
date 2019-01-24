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
    base_url = "https://api.rev.ai/revspeech/{v}/".format(v=version)

    def __init__(self, api_key):
        """Constructor

        :param api_key: api key which authorizes all requests and links them to
            your account. Generated on the settings page of your account
            dashboard on rev.ai
        """
        if not api_key:
            raise ValueError("API Key cannot be empty.")
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': 'Bearer {api_key}'.format(api_key=api_key),
            'User-Agent': 'python_sdk'
        })

    def submit_job_url(self, media_url, options):
        """Submit media given a URL for transcription.
        The audio data is downloaded from the URL.

        :param media_url: web location of the media file
        :param options: JobSubmitOptions object for the job
        :returns: raw response data
        """
        url_jobs = urljoin(self.base_url, "jobs")
        payload = {
            'media_url': media_url,
            'metadata': options.metadata
        }
        if options.callback_url:
            payload['callback_url'] = options.callback_url
        response = self.session.post(url_jobs, json=payload)

        return Job.from_json(response.json())

    def submit_job_local_file(self, filename, options):
        """Submit a local file for transcription.
        Note that the content type is inferred if not provided.

        :param filename: path to a local file on disk
        :param options: JobSubmitOptions object for the job
        :returns: raw response data
        """
        url_jobs = urljoin(self.base_url, "jobs")
        payload = {'metadata': options.metadata}
        if options.callback_url:
            payload['callback_url'] = options.callback_url

        with open(filename, 'rb') as f:
            files = {
                'media': (filename, f),
                'options': (None, json.dumps(payload))
            }
            response = self.session.post(url_jobs, files=files)

        return Job.from_json(response.json())

    def get_job_details(self, id_):
        """View information about a specific job.
        The server will respond with the status and creation date.

        :param id_: id of the job to be requested
        :returns: raw response data
        """
        url_jobs_id = urljoin(self.base_url, "jobs/{id_}".format(id_=id_))

        response = self.session.get(url_jobs_id)

        return Job.from_json(response.json())

    def get_transcript_text(self, id_):
        """Get the transcript of a specific job as json.

        :param id_: id of job to be requested
        :returns: transcript data as text
        """
        url_jobs_transcript = urljoin(
            self.base_url,
            "jobs/{id_}/transcript".format(id_=id_)
        )

        response = self.session.get(
            url_jobs_transcript,
            headers={'Accept': "text/plain"}
        )

        return response.text

    def get_transcript_object(self, id_):
        """Get the transcript of a specific job as json.

        :param id_: id of job to be requested
        :returns: transcript data as a python object
        """
        url_jobs_transcript = urljoin(
            self.base_url,
            "jobs/{id_}/transcript".format(id_=id_)
        )

        response = self.session.get(
            url_jobs_transcript,
            headers={'Accept': 'application/{transcript_version}+json'
                     .format(transcript_version="vnd.rev.transcript.v1.0")}
        )

        return Transcript.from_json(response.json())

    def get_account(self):
        """Get account information, such as remaining balance.
        """
        url_account = urljoin(self.base_url, "account")

        response = self.session.get(url_account)

        return Account.from_json(response.json())
