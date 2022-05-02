# -*- coding: utf-8 -*-
"""Generic client used to interact with our newer style apis"""

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

    def _submit_job(self, payload):
        """Submit a job to the api. This method is special in that it is intended to be hidden by
        the implementation this is done because python standard is to pass options individually
        instead of as an object and our true clients should match this standard

        :param payload: payload to be sent with job request
        :raises: HTTPError
        """
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

    def _get_result_json(self, id_, params):
        """Get the result of a job. This method is special in that it is intended to be hidden by
        the implementation this is done because python standard is to pass options individually
        instead of as an object and our true clients should match this standard

        :param id_: id of job to be requested
        :returns: job result data as raw json
        :raises: HTTPError
        """
        if not id_:
            raise ValueError('id_ must be provided')

        query_params = []
        for key, value in params.items():
            if value is not None:
                query_params.append('{0}={1}'.format(key, value))

        response = self._make_http_request(
            "GET",
            urljoin(self.base_url, 'jobs/{0}/result?{1}'.format(id_, '&'.join(query_params)))
        )

        return response.json()

    def _get_result_object(self, id_, params):
        """Get the result of a job. This method is special in that it is intended to be hidden by
        the implementation this is done because python standard is to pass options individually
        instead of as an object and our true clients should match this standard

        :param id_: id of job to be requested
        :returns: job result data as object
        :raises: HTTPError
        """
        return self.parse_job_result(self._get_result_json(id_, params))

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

    def create_payload_with_source(self, media_url, source_config, metadata, callback_url,
                                   delete_after_seconds, notification_config):
        payload = {}
        if media_url:
            payload['media_url'] = media_url
        if source_config:
            payload['source_config'] = source_config.to_dict()
        self._copy_options(payload, metadata, callback_url, delete_after_seconds,
                           notification_config)
        return payload

    def _enhance_payload(self, payload, metadata, callback_url, delete_after_seconds,
                         notification_config):
        enhanced = payload.copy()
        self._copy_options(enhanced, metadata, callback_url, delete_after_seconds,
                           notification_config)
        return enhanced

    @staticmethod
    def _copy_options(payload, metadata, callback_url, delete_after_seconds,
                      notification_config):
        if metadata:
            payload['metadata'] = metadata
        if callback_url:
            payload['callback_url'] = callback_url
        if delete_after_seconds is not None:
            payload['delete_after_seconds'] = delete_after_seconds
        if notification_config:
            payload['notification_config'] = notification_config.to_dict()
