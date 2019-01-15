# -*- coding: utf-8 -*-
"""Account Model"""

class Account:
	def __init__(self, email, balance_seconds):
        """
        :param email: email associated with the account
        :param balance_seconds: seconds of audio this account has the credits to transcribe
        """
		self.email = email
		self.balance_seconds = balance_seconds

	@classmethod
	def from_json(cls, json):
		"""Alternate constructor used for parsing json"""
		return cls(
			json["email"],
			json["balance_seconds"]
		)