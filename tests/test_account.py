try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
import pytest
from src.rev_ai.models import Account
from src.rev_ai.apiclient import RevAiAPIClient


@pytest.mark.usefixtures("mockclient")
class TestAccountEndpoints():
    def test_get_account_success(self, mockclient):
        data = {
            "email": "test@example.com",
            "balance_seconds": 10
        }
        mockclient.session.get.return_value.json.return_value = data

        res = mockclient.get_account()

        assert res == Account(data.get('email'), data.get('balance_seconds'))
        mockclient.session.get.assert_called_once_with(
            urljoin(RevAiAPIClient.base_url, "account")
        )

    def test_get_account_not_authorized_error(self, mockclient):
        data = {
            "title": "Authorization has been denied for this request",
            "status": 401
        }
        mockclient.session.get.return_value.json.return_value = data

        with pytest.raises(KeyError):
            mockclient.get_account()
