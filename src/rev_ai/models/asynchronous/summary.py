from typing import List, Dict


class Summary:
    """Transcript summary model."""
    def __init__(
            self,
            summary: str,
            bullet_points: List[str]):
        self.summary = summary
        self.bullet_points = bullet_points

    @classmethod
    def from_json(cls, json):
        return cls(
            json.get('summary'),
            json.get('bullet_points')
        )
