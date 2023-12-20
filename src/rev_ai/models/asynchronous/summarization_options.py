from rev_ai.models.asynchronous.summarization_formatting_options import SummarizationFormattingOptions
from rev_ai.models.asynchronous.summarization_job_status import SummarizationJobStatus
from rev_ai.models.nlp_model import NlpModel


class SummarizationOptions:
    def __init__(
            self,
            prompt: str = None,
            model: NlpModel = None,
            formattingType: SummarizationFormattingOptions = None
    ):
        self.prompt = prompt
        self.model = model
        self.type = formattingType

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
    def __init__(
            self,
            prompt: str = None,
            model: NlpModel = None,
            formattingType: SummarizationFormattingOptions = None,
            status: SummarizationJobStatus = None,
            completed_on: str = None,
            failure: str = None
    ):
        super().__init__(prompt, model, formattingType)
        self.status = status
        self.completed_on = completed_on
        self.failure = failure

    @classmethod
    def from_json(cls, json):
        return cls(
            json.get('prompt'),
            json.get('model'),
            json.get('type'),
            json.get('status'),
            json.get('completed_on'),
            json.get('failure')
        )
