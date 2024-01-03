from .summarization_formatting_options import SummarizationFormattingOptions
from .summarization_job_status import SummarizationJobStatus
from .summarization_model import SummarizationModel


class SummarizationOptions:
    """Summarization request options."""

    def __init__(
            self,
            prompt: str = None,
            model: SummarizationModel = None,
            formatting_type: SummarizationFormattingOptions = None):
        self.prompt = prompt
        self.model = model
        self.type = formatting_type

    def to_dict(self):
        """Returns the raw form of the url data object as the api
        expects them"""
        dict_result = {}
        if self.prompt:
            dict_result['prompt'] = self.prompt
        if self.model:
            dict_result['model'] = self.model
        if self.type:
            dict_result['type'] = self.type

        return dict_result


class Summarization(SummarizationOptions):
    """Summarization options."""

    def __init__(
            self,
            prompt: str = None,
            model: SummarizationModel = None,
            formatting_type: SummarizationFormattingOptions = None,
            status: SummarizationJobStatus = None,
            completed_on: str = None,
            failure: str = None):
        super().__init__(prompt, model, formatting_type)
        self.status = status
        self.completed_on = completed_on
        self.failure = failure

    @classmethod
    def from_json(cls, json):
        if json is None:
            return None

        return cls(
            json.get('prompt'),
            json.get('model'),
            json.get('type'),
            json.get('status'),
            json.get('completed_on'),
            json.get('failure')
        )
