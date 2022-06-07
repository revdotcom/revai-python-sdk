def get_error_test_cases(errors):
    return [ERRORS.get(e) for e in errors]


ERRORS = {
    'invalid-parameters': {
        "type": "https://www.rev.ai/api/v1/errors/invalid-parameters",
        "title": "Your request parameters did not validate",
        "status": 400
    },
    'unauthorized': {
        "title": "Authorization has been denied for this request",
        "status": 401
    },
    'forbidden': {
        "status": 403,
        "error": "The client is forbidden to submit that request"
    },
    'job-not-found': {
        "type": "https://www.rev.ai/api/v1/errors/job-not-found",
        "title": "could not find job",
        "status": 404
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
