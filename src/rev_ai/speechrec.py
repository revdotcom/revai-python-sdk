# -*- coding: utf-8 -*-
"""Speech recognition tools for using rev.ai
"""
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
import os
import requests
import logging
import json
from models import *

LOG = logging.getLogger(__name__)

class RevSpeechAPIClient:
    """Client which implements rev.ai API"""

    VERSION = "v1"
    """Default version of rev.ai"""

    BASE_URL = "https://api.rev.ai/revspeech/{v}/".format(v=VERSION)
    """Default address of the API"""

    def __init__(
        self,
        api_key
    ):
        """
        Constructor

        :param api_key: api key which authorizes all requests and links them to your account.
            Generated on the settings page of your account dashboard on rev.ai
        """
        if not api_key:
            raise ValueError("API Key cannot be empty.")
        self.s = requests.Session()
        self.s.headers.update({
            'Authorization': 'Bearer {api_key}'.format(api_key=api_key)
        })


    def submit_job_url(
        self, 
        media_url, 
        options
    ):
        """Submit a web URL for transcription.
        The audio data is downloaded from the URL.

        :param media_url: web location of the media file
        :param options: JobSubmitOptions object for the job
        :returns: raw response data
        """
        url_jobs = urljoin(self.BASE_URL, "jobs")
        payload = {
            'media_url': media_url,
            'metadata': options.metadata
        }
        if options.callback_url:
            payload['callback_url'] = options.callback_url
        response = self.s.post(url_jobs, json=payload)

        if (response.status_code == 200):
            return Job.from_json(response.json())
        elif (response.status_code == 400):
            return InvalidParametersError.from_json(response.json())
        elif (response.status_code == 403):
            return InsufficientBalanceError.from_json(response.json())
        else:
            return ApiError.from_json(response.json())

    def submit_job_local_file(
        self, 
        filename, 
        options, 
        content_type=None
    ):
        """Submit a local file for transcription.
        Note that the content type is inferred if not provided.

        :param filename: path to a local file on disk
        :param content_type: MIME content type of file being sent
        :param options: JobSubmitOptions object for the job
        :returns: raw response data
        """
        url_jobs = urljoin(self.BASE_URL, "jobs")
        LOG.debug('Using content type: "%s".', content_type)
        payload = {'metadata': options.metadata}
        if options.callback_url:
            payload['callback_url'] = options.callback_url

        with open(filename, 'rb') as f:
            files = {
                'media': (filename, f, content_type),
                'options': (None, json.dumps(payload))
            }
            response = self.s.post(url_jobs, files=files)

        if (response.status_code == 200):
            return Job.from_json(response.json())
        elif (response.status_code == 400):
            return InvalidParametersError.from_json(response.json())
        elif (response.status_code == 403):
            return InsufficientBalanceError.from_json(response.json())
        else:
            return ApiError.from_json(response.json())        

    def view_job(
        self, 
        id_
    ):
        """View information about a specific job.
        The server will respond with the status and creation date.

        :param id_: id that the server gave you
        :returns: raw response data
        """
        url_jobs_id = urljoin(self.BASE_URL, "jobs/{id_}".format(id_=id_))

        response = self.s.get(url_jobs_id)

        return Job.from_json(response.json())

    def get_transcript_as_text(
        self, 
        id_
    ):
        """Get the transcript of a specific job as json.

        :param id_: id that the server gave you
        :returns: transcript data as text
        """
        url_jobs_transcript = urljoin(self.BASE_URL,
            "jobs/{id_}/transcript".format(id_=id_))

        response = self.s.get(url_jobs_transcript,
                              headers={'Accept': "text/plain"})

        return response.text

    def get_transcript_as_json(
        self, 
        id_
    ):
        """Get the transcript of a specific job as json.

        :param id_: id that the server gave you
        :returns: transcript data as JSON
        """
        url_jobs_transcript = urljoin(self.BASE_URL,
            "jobs/{id_}/transcript".format(id_=id_))

        response = self.s.get(url_jobs_transcript,
            headers={'Accept': 'application/{version}+json'
                 .format(version="vnd.rev.transcript.v1.0")})

        return response.json()

    def get_account(
        self
    ):
        """Get account information, such as remaining balance.
        """
        url_account = urljoin(self.BASE_URL, "account")

        response = self.s.get(url_account)

        return response.json()

client = RevSpeechAPIClient("02cD6t8ixL12YX8BFwHbNmuQa05GeD3GwAyjuiDStTC_FAEUCFiLvJkge4JSPRzcrh1siMmWv4RthnTZS1KfIvHCMSXP4")
options = JobSubmitOptions()
print(client.submit_job_url("", options))
