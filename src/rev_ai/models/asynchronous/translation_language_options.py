from .summarization_job_status import SummarizationJobStatus
from ..nlp_model import NlpModel


class TranslationLanguageOptions:
    def __init__(
            self,
            language: str = None,
            model: NlpModel = None
    ):
        self.language = language
        self.model = model

    def to_dict(self):
        """Returns the raw form of the url data object as the api
        expects them"""
        dict_result = {}
        if self.language:
            dict_result['language'] = self.language
        if self.model:
            dict_result['model'] = self.model

        return dict_result


class TranslationLanguage(TranslationLanguageOptions):
    def __init__(
            self,
            language: str = None,
            model: NlpModel = None,
            status: SummarizationJobStatus = None,
            failure: str = None

    ):
        super().__init__(language, model)
        self.status = status
        self.failure = failure

    @classmethod
    def from_json(cls, json):
        return cls(
            json.get('language'),
            json.get('model'),
            json.get('status'),
            json.get('failure')
        )
