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

LOG = logging.getLogger(__name__)


class RevSpeechAPI:
    VERSION = "v1beta"
    BASE_URL = "https://api.rev.ai/revspeech/{v}/".format(v=VERSION)

    def __init__(self, api_key, use_stage=False):
        if not api_key:
            raise ValueError("API Key cannot be empty.")
        self.s = requests.Session()
        self.s.headers.update({
            'Authorization': 'Bearer {api_key}'.format(api_key=api_key)
        })
        if use_stage:
            self.BASE_URL = ("https://api-stage.rev.ai/revspeech/{v}/"
                             .format(v=VERSION))


    def submit_job_url(self, media_url, metadata=""):
        """Submit a web URL for transcription.
        The audio data is downloaded from the URL.

        :param media_url: web location of the media file
        :param metadata: info to associate with the transcription job
        :returns: raw response data
        """
        url_jobs = urljoin(self.BASE_URL, "jobs")
        payload = {
            'media_url': media_url,
            'metadata': metadata
        }

        response = self.s.post(url_jobs, json=payload)

        return response.json()

    def submit_job_local_file(self, filename,
                              media_type="audio", content_type=None):
        """Submit a local file for transcription.
        Note that the content type is inferred if not provided.

        :param filename: path to a local file on disk
        :param media_type: "audio" or "video"
        :param content_type: explicitly specify request content type
        :returns: raw response data
        """
        url_jobs = urljoin(self.BASE_URL, "jobs")
        if media_type not in {"audio", "video"}:
            raise ValueError("media_type must be audio or video")
        _base, extension = os.path.splitext(filename)
        content_type = content_type or media_type + '/' + extension
        LOG.debug('Using content type: "%s".', content_type)

        with open(filename, 'rb') as f:
            files = {
                'media': (filename, f, content_type)
            }
            response = self.s.post(url_jobs, files=files)

        return response.json()

    def view_job(self, id_):
        """View information about a specific job.
        The server will respond with the status and creation date.

        :param id_: id that the server gave you
        :returns: raw response data
        """
        url_jobs_id = urljoin(self.BASE_URL, "jobs/{id_}".format(id_=id_))

        response = self.s.get(url_jobs_id)

        return response.json()

    def get_transcript(self, id_, use_json=True):
        """Get account information, such as remaining balance.

        :param id_: id that the server gave you
        :param use_json: get result as structured JSON, instead of cleartext
        :returns: transcript data (txt or JSON)
        """
        url_jobs_transcript = urljoin(self.BASE_URL,
                                      "jobs/{id_}/transcript".format(id_=id_))
        if use_json:
            content_type_accept = ('application/{version}+json'
                                   .format(version="vnd.rev.transcript.v1.0"))
        else:
            content_type_accept = 'text/plain'

        response = self.s.get(url_jobs_transcript,
                              headers={'Accept': content_type_accept})

        return response.json() if use_json else response.text

    def get_account(self):
        """Get account information, such as remaining balance.
        """
        url_account = urljoin(self.BASE_URL, "account")

        response = self.s.get(url_account)

        return response.json()
