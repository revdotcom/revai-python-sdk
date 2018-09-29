# -*- coding: utf-8 -*-
"""Speech recognition tools for using rev.ai
"""
import requests
import os


class RevSpeechAPI:
    BASE_URL = "https://api.rev.ai/revspeech/{version}".format(version="v1beta")

    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API Key cannot be empty")
        self.HEADERS = {'Authorization':
                        'Bearer {api_key}'.format(api_key=api_key)}

    def submit_job_url(self, media_url, metadata=" "):
        url = os.path.join(self.BASE_URL, "jobs")
        payload = {'media_url': media_url,
                   'metadata': metadata}
        request = requests.post(url, headers=self.HEADERS, json=payload)

        response_body = request.json()
        return response_body

    def submit_job_local_file(self, file, media_type="audio"):
        url = os.path.join(self.BASE_URL, "jobs")
        if media_type != "audio" and media_type != "video":
            raise ValueError("media_type must be audio or video")
        filename, file_extension = os.path.splitext(file)
        with open(file, 'rb') as fo:
            files = {'media': (file, fo,  media_type + '/' + file_extension)}
            request = requests.post(url, headers=self.HEADERS, files=files)

        response_body = request.json()
        return response_body

    def view_job(self, id):
        url = os.path.join(self.BASE_URL, "jobs", id)
        request = requests.get(url, headers=self.HEADERS)

        response_body = request.json()
        return response_body

    def get_transcript(self, id, response_type=".json"):
        url = os.path.join(self.BASE_URL, "jobs", id, 'transcript')
        headers = self.HEADERS.copy()
        if response_type == ".json":
            headers['Accept'] = 'application/{version}+json'.format(version="vnd.rev.transcript.v1.0")
        elif response_type == ".txt":
            headers['Accept'] = 'text/plain'
        else:
            raise ValueError("response_type must be .json or .txt")
        request = requests.get(url, headers=headers)

        response_body = request.json() if response_type == ".json" else request.text
        return response_body

    def get_account(self):
        url = os.path.join(self.BASE_URL, "account")
        request = requests.get(url, headers=self.HEADERS)

        response_body = request.json()
        return response_body
