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
            duration_seconds=None,
            delete_after_seconds=None,
            skip_diarization=None,
            skip_punctuation=None,
            remove_disfluencies=None,
            filter_profanity=None,
            custom_vocabulary_id=None,
            speaker_channels_count=None,
            language=None,
            transcriber=None,
            verbatim=None,
            rush=None,
            segments_to_transcribe=None):
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
        :param delete_after_seconds: seconds before deletion if provided
        :param skip_diarization: whether to skip diarization if provided
        :param skip_punctuation: whether to skip punctuation if provided
        :param remove_disfluencies: whether to remove disfluencies if provided
        :param filter_profanity: whether to filter profanity if provided
        :param custom_vocabulary_id: custom vocabulary id if provided
        :param speaker_channels_count: speaker channels count if provided
        :param language: language of job
        :param transcriber: transcriber to use for job
        :param verbatim: whether to transcribe verbatim if provided for human transcription
        :param rush: whether to transcribe with rush if provided for human transcription
        :param segments_to_transcribe: segments to transcribe if provided for human transcription
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
        self.delete_after_seconds = delete_after_seconds
        self.skip_diarization = skip_diarization
        self.skip_punctuation = skip_punctuation
        self.remove_disfluencies = remove_disfluencies
        self.filter_profanity = filter_profanity
        self.custom_vocabulary_id = custom_vocabulary_id
        self.speaker_channels_count = speaker_channels_count
        self.language = language
        self.transcriber = transcriber
        self.verbatim = verbatim
        self.rush = rush
        self.segments_to_transcribe = segments_to_transcribe

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
            name=json.get('name'),
            callback_url=json.get('callback_url'),
            metadata=json.get('metadata'),
            media_url=json.get('media_url'),
            failure=json.get('failure'),
            failure_detail=json.get('failure_detail'),
            duration_seconds=json.get('duration_seconds'),
            delete_after_seconds=json.get('delete_after_seconds'),
            skip_diarization=json.get('skip_diarization'),
            skip_punctuation=json.get('skip_punctuation'),
            remove_disfluencies=json.get('remove_disfluencies'),
            filter_profanity=json.get('filter_profanity'),
            custom_vocabulary_id=json.get('custom_vocabulary_id'),
            speaker_channels_count=json.get('speaker_channels_count'),
            language=json.get('language'),
            transcriber=json.get('transcriber'),
            verbatim=json.get('verbatim'),
            rush=json.get('rush'),
            segments_to_transcribe=json.get('segments_to_transcribe')
        )
