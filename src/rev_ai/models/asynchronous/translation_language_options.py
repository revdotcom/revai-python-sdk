from .translation_job_status import TranslationJobStatus
from .translation_model import TranslationModel


class TranslationLanguageOptions:
    """Translation language request options."""
    def __init__(
            self,
            language: str = None,
            model: TranslationModel = None):
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
    """Translation language options."""
    def __init__(
            self,
            language: str = None,
            model: TranslationModel = None,
            status: TranslationJobStatus = None,
            failure: str = None):
        super().__init__(language, model)
        self.status = status
        self.failure = failure

    @classmethod
    def from_json(cls, json):
        if json is None:
            return None
        return cls(
            json.get('language'),
            json.get('model'),
            json.get('status'),
            json.get('failure')
        )
