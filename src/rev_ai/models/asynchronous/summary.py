class Summary:
    def __init__(
            self,
            summary:str,
            bullet_points: list[str],
    ):
        self.summary = summary
        self.bullet_points = bullet_points

    @classmethod
    def from_json(cls, json):
        return cls(
            json.get('summary'),
            json.get('bullet_points')
        )
