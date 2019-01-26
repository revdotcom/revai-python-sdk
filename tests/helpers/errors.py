def get_error_test_cases(errors):
    return [ERRORS.get(e) for e in errors]


ERRORS = {
    'invalid-parameters': {
        "parameter": {
            "example": [
                "The example field is required"
            ]
        },
        "type": "https://www.rev.ai/api/v1/errors/invalid-parameters",
        "title": "Your request parameters didn't validate",
        "status": 400
    },
    'unauthorized': {
        "title": "Authorization has been denied for this request",
        "status": 401
    },
    'job-not-found': {
        "type": "https://www.rev.ai/api/v1/errors/job-not-found",
        "title": "could not find job",
        "status": 404
    },
    'out-of-credit': {
        "title": "You do not have enough credits",
        "type": "https://www.rev.ai/api/v1/errors/out-of-credit",
        "detail": "You have only 60 seconds remaining",
        "current_balance": 60,
        "status": 403
    },
    'invalid-job-state': {
        "allowed_values": [
            "transcribed"
        ],
        "current_value": "in_progress",
        "type": "https://rev.ai/api/v1/errors/invalid-job-state",
        "title": "Job is in invalid state",
        "detail": "Job is in invalid state to obtain the transcript",
        "status": 409
    }
}
