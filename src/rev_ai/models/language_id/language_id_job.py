# -*- coding: utf-8 -*-
"""Job model"""

from ..asynchronous.job_status import JobStatus


class LanguageIdentificationJob:
    def __init__(
            self, id_, created_on, status,
            completed_on=None,
            callback_url=None,
            metadata=None,
            media_url=None,
            failure=None,
            failure_detail=None,
            processed_duration_seconds=None,
            delete_after_seconds=None):
        """
        :param id_: unique id of job
        :param created_on: date and time at which this job was started
        :param status: current job status 'IN_PROGRESS', 'COMPLETED', or 'FAILED'
        :param completed_on: date and time at which this job finished being processed
        :param callback_url: callback_url if provided
        :param metadata: metadata if provided
        :param media_url: url of transcribed media if job was submitted this way
        :param failure: type of failure if job has failed
        :param failure_detail: more detailed failure message if job has failed
        :param processed_duration_seconds: duration of file processed in seconds
        :param delete_after_seconds: seconds before deletion if provided
        """

        self.id = id_
        self.created_on = created_on
        self.status = status
        self.completed_on = completed_on
        self.callback_url = callback_url
        self.metadata = metadata
        self.media_url = media_url
        self.failure = failure
        self.failure_detail = failure_detail
        self.processed_duration_seconds = processed_duration_seconds
        self.delete_after_seconds = delete_after_seconds

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
            completed_on=json.get('completed_on'),
            callback_url=json.get('callback_url'),
            metadata=json.get('metadata'),
            media_url=json.get('media_url'),
            failure=json.get('failure'),
            failure_detail=json.get('failure_detail'),
            processed_duration_seconds=json.get('processed_duration_seconds'),
            delete_after_seconds=json.get('delete_after_seconds'),
        )
