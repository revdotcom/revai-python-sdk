# -*- coding: utf-8 -*-
"""Job model"""

from ...asynchronous.job_status import JobStatus


class SentimentAnalysisJob:
    def __init__(
            self, id_, created_on, status,
            completed_on=None,
            callback_url=None,
            metadata=None,
            failure=None,
            failure_detail=None,
            word_count=None,
            delete_after_seconds=None):
        """
        :param id_: unique id of job
        :param created_on: date and time at which this job was started
        :param status: current job status 'IN_PROGRESS', 'COMPLETED',
                       or 'FAILED'
        :param completed_on: date and time at which this job finished
                             being processed
        :param callback_url: callback_url if provided
        :param metadata: metadata if provided
        :param failure: type of failure if job has failed
        :param failure_detail: more detailed failure message if job has failed
        :param word_count: count of words in job
        :param delete_after_seconds: seconds before deletion if provided
        """

        self.id = id_
        self.created_on = created_on
        self.status = status
        self.completed_on = completed_on
        self.callback_url = callback_url,
        self.metadata = metadata
        self.failure = failure
        self.failure_detail = failure_detail
        self.delete_after_seconds = delete_after_seconds
        self.word_count = word_count

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
            failure=json.get('failure'),
            failure_detail=json.get('failure_detail'),
            word_count=json.get('word_count'),
            delete_after_seconds=json.get('delete_after_seconds'),
        )
