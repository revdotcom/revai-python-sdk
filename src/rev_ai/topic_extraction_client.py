from .generic_api_client import GenericApiClient
from .models import TopicExtractionJob, TopicExtractionResult


class TopicExtractionClient(GenericApiClient):
    """Client for interacting with the Rev AI topic extraction api"""

    # Default version of Rev AI topic extraction api
    api_version = 'v1beta'

    # Default api name of Rev AI topic extraction api
    api_name = 'topic_extraction'

    def __init__(self, access_token):
        """Constructor

        :param access_token: access token which authorizes all requests and links them to your
                             account. Generated on the settings page of your account dashboard
                             on Rev AI.
        """

        GenericApiClient.__init__(self, access_token, self.api_name, self.api_version,
                                  TopicExtractionJob.from_json, TopicExtractionResult.from_json)

    def submit_job(self,
                   text=None,
                   json=None,
                   metadata=None,
                   callback_url=None,
                   delete_after_seconds=None,
                   language=None):
        """Submit a job to the Rev AI topic extraction api. Takes either a plain text string or
        Transcript object

        :param text: Plain text string to be run through topic extraction
        :param json: Transcript object from the Rev AI async transcription client to be run through
                     topic extraction
        :param metadata: info to associate with the transcription job
        :param callback_url: callback url to invoke on job completion as
                             a webhook
        :param delete_after_seconds: number of seconds after job completion when job is auto-deleted
        :param language: specify language using the one of the supported ISO 639-1 (2-letter) or
            ISO 639-3 (3-letter) language codes as defined in the API Reference
        :returns: TopicExtractionJob object
        :raises: HTTPError
        """
        options = {}
        if text:
            options['text'] = text
        if json:
            options['json'] = json.to_dict()
        return self._submit_job(options, metadata, callback_url, delete_after_seconds, language)
