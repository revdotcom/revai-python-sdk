class Account:
	def __init__(
		self,
		email,
		balance_seconds
	):
		self.email = email
		self.balance_seconds = balance_seconds

	@classmethod
	def from_json(
		cls,
		json
	):
		return cls(
			json["email"],
			json["balance_seconds"]
		)