# -*- coding: utf-8 -*-
"""Account model"""


class Account:
    def __init__(self, email, balance_seconds):
        """
        :param email: email associated with the account
        :param balance_seconds: seconds of audio this account has the credits to transcribe
        """
        self.email = email
        self.balance_seconds = balance_seconds

    def __eq__(self, other):
        """Override default equality operator"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls(json['email'], json['balance_seconds'])
