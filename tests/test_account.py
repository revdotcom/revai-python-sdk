# -*- coding: utf-8 -*-
"""Unit tests for account endpoints"""

import pytest
from src.rev_ai.apiclient import RevAiAPIClient
from src.rev_ai.models import Account

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


@pytest.mark.usefixtures("mockclient")
class TestAccountEndpoints():
    def test_get_account_success(self, mockclient):
        email = "text@example.com"
        seconds = 10
        data = {"email": email, "balance_seconds": seconds}
        mockclient.session.get.return_value.json.return_value = data

        res = mockclient.get_account()

        assert res == Account(email, seconds)
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
