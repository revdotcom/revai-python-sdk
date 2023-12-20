from .translation_language_options import TranslationLanguageOptions, TranslationLanguage


class TranslationOptions:
    def __init__(
            self,
            target_languages: list[TranslationLanguageOptions]
    ):
        self.target_languages = target_languages

    def to_dict(self):
        """Returns the raw form of the url data object as the api
        expects them"""
        dict_result = {}
        dict_result["target_languages"] = [tl.to_dict() for tl in self.target_languages]

        return dict_result


class Translation(TranslationOptions):
    def __init__(
            self,
            target_languages: list[TranslationLanguageOptions],
            completed_on: str = None,
    ):
        super().__init__(target_languages)
        self.completed_on = completed_on

    @classmethod
    def from_json(cls, json):
        return cls(
            [TranslationLanguage.from_json(tl) for tl in json.get('target_languages')],
            json.get('completed_on')
        )
