class CustomerUrlData:
    """Object used to contain a url provided by the customer along with any other related information,
     such as authentication headers."""

    def __init__(self, url, auth_headers = None):
        """Constructor
        :param url: customer provided url
        :param auth_headers: customer provided headers to access the url
        """
        self.url = url
        self.auth_headers = auth_headers

    def to_dict(self):
        """Returns the raw form of the url data object as the api
        expects them"""
        dict_result = {'url': self.url}
        if self.auth_headers:
            dict_result['auth_headers'] = self.auth_headers
        return dict_result
