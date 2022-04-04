from .baseclient import BaseClient

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class GenericApiClient(BaseClient):
    """Generic client which handles logic for making requests to almost any Rev AI Api.
    Intended to be inherited and extended by a specific client per API"""

    def __init__(self, access_token, api_name, api_version, parse_job_info, parse_job_result):
        """Constructor

        :param access_token: access token which authorizes all requests and links them to your
                             account. Generated on the settings page of your account dashboard
                             on Rev AI.
        :param api_name: name of the api to submit to
        :param api_version: version of the api to submit to
        :param parse_job_info: method to be used to parse job information
        :param parse_job_result: method to be used to parse job results
        """

        BaseClient.__init__(self, access_token)
        self.base_url = 'https://api.rev.ai/{0}/{1}/'.format(api_name, api_version)
        self.parse_job_info = parse_job_info
        self.parse_job_result = parse_job_result

    def _submit_job(self, payload,
                    metadata=None,
                    callback_url=None,
                    delete_after_seconds=None,
                    language=None):
        """Submit a job to the api. This method is special in that it is intended to be hidden by
        the implementation this is done because python standard is to pass options individually
        instead of as an object and our true clients should match this standard

        :param payload: special options for the specific api being used
        :param metadata: info to associate with the transcription job
        :param callback_url: callback url to invoke on job completion as
                             a webhook
        :param delete_after_seconds: number of seconds after job completion when job is auto-deleted
        :param language: specify language using the one of the supported ISO 639-1 (2-letter) or
            ISO 639-3 (3-letter) language codes as defined in the API Reference
        :returns: Job info object
        :raises: HTTPError
        """
        if metadata:
            payload['metadata'] = metadata
        if callback_url:
            payload['callback_url'] = callback_url
        if delete_after_seconds is not None:
            payload['delete_after_seconds'] = delete_after_seconds
        if language:
            payload['language'] = language

        response = self._make_http_request(
            "POST",
            urljoin(self.base_url, 'jobs'),
            json=payload
        )

        return self.parse_job_info(response.json())

    def get_job_details(self, id_):
        """View information about a specific job.
        The server will respond with the status and creation date.

        :param id_: id of the job to be requested
        :returns: Job info object
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')

        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, 'jobs/{}'.format(id_))
        )

        return self.parse_job_info(response.json())

    def get_list_of_jobs(self, limit=None, starting_after=None):
        """Get a list of jobs submitted within the last 30 days in reverse
        chronological order up to the provided limit number of jobs per call.
        Pagination is supported via passing the last job id from previous call into starting_after.

        :param limit: optional, limits the number of jobs returned,
                      if none, a default of 100 jobs is returned, max limit if 1000
        :param starting_after: optional, returns jobs created after the job with this id,
                               exclusive (job with this id is not included)
        :returns: list of jobs response data
        :raises: HTTPError
        """
        params = []
        if limit is not None:
            params.append('limit={}'.format(limit))
        if starting_after is not None:
            params.append('starting_after={}'.format(starting_after))

        query = '?{}'.format('&'.join(params))
        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, 'jobs{}'.format(query))
        )

        return [self.parse_job_info(job) for job in response.json()]

    def get_result_object(self, id_):
        """Get the result of a specific job

        :param id_: id of job to be requested
        :returns: job result data as object
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')

        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, 'jobs/{}/result'.format(id_))
        )

        return self.parse_job_result(response.json())

    def get_result_json(self, id_):
        """Get the result of a specific job

        :param id_: id of job to be requested
        :returns: job result data as raw json
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')

        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, 'jobs/{}/result'.format(id_))
        )

        return response.json()

    def delete_job(self, id_):
        """Delete a specific job
        All data related to the job, such as input media and result, will be permanently
        deleted. A job can only by deleted once it's completed.

        :param id_: id of job to be deleted
        :returns: None if job was successfully deleted
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')

        self._make_http_request(
            "DELETE",
            urljoin(self.base_url, 'jobs/{}'.format(id_)),
        )

        return
