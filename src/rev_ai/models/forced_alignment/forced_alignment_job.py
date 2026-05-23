# -*- coding: utf-8 -*-
"""Contains ForcedAlignmentJob dataclass"""

from typing import Dict, Any
from ..asynchronous.job_status import JobStatus


class ForcedAlignmentJob:
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
        """Dataclass containing information about a Rev AI forced alignment job

        :param id: unique identifier for this job
        :param status: current job status
        :param created_on: date and time at which this job was created
        :param completed_on: date and time at which this job was completed
        :param metadata: customer-provided metadata
        :param type: type of job (always "alignment")
        :param media_url: URL of the media to be aligned
        :param failure: details about job failure if status is "failed"
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
    def from_json(cls, json: Dict[str, Any]) -> 'ForcedAlignmentJob':
        """Alternate constructor used for parsing json

        :param json: json dictionary to convert
        :returns: ForcedAlignmentJob
        """
        return cls(
            id_=json['id'],
            created_on=json['created_on'],
            status=JobStatus.from_string(json['status']),
            completed_on=json.get('completed_on'),
            callback_url=json.get('callback_url'),
            metadata=json.get('metadata'),
            media_url=json.get('media_url'),
            failure=json.get('failure'),
            failure_detail=json.get('failure_detail'),
            processed_duration_seconds=json.get('processed_duration_seconds'),
            delete_after_seconds=json.get('delete_after_seconds')
        )
