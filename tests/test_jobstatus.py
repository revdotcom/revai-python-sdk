from rev_ai import JobStatus


class TestJobStatus:
    def test_backward_compat_job_status_equals_numeric(self):
        assert JobStatus.IN_PROGRESS == JobStatus.IN_PROGRESS
        assert JobStatus.IN_PROGRESS.value == 1
        assert JobStatus.IN_PROGRESS.name == 'IN_PROGRESS'
        assert JobStatus.from_string('in_progress') == JobStatus.IN_PROGRESS
        assert JobStatus.from_string('IN_PROGRESS') == JobStatus.IN_PROGRESS

        assert JobStatus.TRANSCRIBED == JobStatus.TRANSCRIBED
        assert JobStatus.TRANSCRIBED.value == 2
        assert JobStatus.TRANSCRIBED.name == 'TRANSCRIBED'
        assert JobStatus.from_string('transcribed') == JobStatus.TRANSCRIBED
        assert JobStatus.from_string('TRANSCRIBED') == JobStatus.TRANSCRIBED



        assert JobStatus.FAILED == JobStatus.FAILED
        assert JobStatus.FAILED.value == 3
        assert JobStatus.FAILED.name == 'FAILED'
        assert JobStatus.from_string('failed') == JobStatus.FAILED
        assert JobStatus.from_string('FAILED') == JobStatus.FAILED



        assert JobStatus.COMPLETED == JobStatus.COMPLETED
        assert JobStatus.COMPLETED.value == 4
        assert JobStatus.COMPLETED.name == 'COMPLETED'
        assert JobStatus.from_string('completed') == JobStatus.COMPLETED
        assert JobStatus.from_string('COMPLETED') == JobStatus.COMPLETED
