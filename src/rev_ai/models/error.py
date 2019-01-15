class ProblemDetail:
	def __init__(
		self,
		status,
		type_,
		title,
		detail
	):
		self.status = status
		self.type = type_
		self.title = title
		self.detail = detail

class ApiError:
	def __init__(
		self,
		problem_details
	):
		self.problem_details = problem_details

	@classmethod
	def from_json(
		cls,
		json
	):
		details = ProblemDetail(
			json.get("status"),
			json.get("type"),
			json["title"],
			json.get("detail")
		)
		return cls(
			details
		)

class InsufficientBalanceError(ApiError):
	def __init__(
		self,
		problem_details,
		current_balance
	):
		ApiError.__init__(self, problem_details)
		self.current_balance = current_balance

	@classmethod
	def from_json(
		cls,
		json
	):
		details = ProblemDetail(
			json.get("status"),
			json["type"],
			json["title"],
			json.get("detail")
		)
		return cls(
			details,
			json["current_balance"]
		)

class InvalidParametersError(ApiError):
	def __init__(
		self,
		problem_details,
		parameters
	):
		ApiError.__init__(self, problem_details)
		self.parameters = parameters

	@classmethod
	def from_json(
		cls,
		json
	):
		details = ProblemDetail(
			json.get("status"),
			json["type"],
			json["title"],
			json.get("detail")
		)
		return cls(
			details,
			json["parameters"]
		)

class InvalidValueError(ApiError):
	def __init__(
		self,
		problem_details,
		allowed_values,
		current_value
	):
		ApiError.__init__(self, problem_details)
		self.allowed_values = allowed_values
		self.current_value = current_value

	@classmethod
	def from_json(
		cls,
		json
	):
		details = ProblemDetail(
			json.get("status"),
			json["type"],
			json["title"],
			json.get("detail")
		)
		return cls(
			details,
			json["allowed_values"],
			json["current_value"]
		)