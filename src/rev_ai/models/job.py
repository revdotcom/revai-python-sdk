# -*- coding: utf-8 -*-
"""Job model"""

from .job_status import JobStatus


class Job:
    def __init__(
            self, id_, created_on, status,
            completed_on=None,
            name=None,
            callback_url=None,
            metadata=None,
            media_url=None,
            failure=None,
            failure_detail=None,
            duration_seconds=None):
        """
        :param id_: unique id of job
        :param created_on: date and time at which this job was started
        :param status: current job status 'IN_PROGRESS', 'TRANSCRIBED',
                       or 'FAILED'
        :param completed_on: date and time at which this job finished
                             being transcribed
        :param name: name of submitted file if local file was used
        :param callback_url: callback_url if provided
        :param metadata: metadata if provided
        :param media_url: url of transcribed media if job was submitted
                          this way
        :param failure: type of failure if job has failed
        :param failure_detail: more detailed failure message if job has failed
        :param duration_seconds: duration of submitted file in seconds
        """
        self.id = id_
        self.created_on = created_on
        self.status = status
        self.completed_on = completed_on
        self.name = name
        self.callback_url = callback_url,
        self.metadata = metadata
        self.media_url = media_url
        self.failure = failure
        self.failure_detail = failure_detail
        self.duration_seconds = duration_seconds

    def __eq__(self, other):
        """Override default equality operator"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls(
            json['id'],
            json['created_on'],
            JobStatus.from_string(json['status']),
            json.get('completed_on'),
            json.get('name'),
            json.get('callback_url'),
            json.get('metadata'),
            json.get('media_url'),
            json.get('failure'),
            json.get('failure_detail'),
            json.get('duration_seconds')
        )
