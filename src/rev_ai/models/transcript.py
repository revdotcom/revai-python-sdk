class Transcript:
    def __init__(self, monologues):
        self.monologues = monologues

    @classmethod
    def from_json(self, json):
        """Alternate constructor used for parsing json"""
        return cls(
            [Monologue.from_json(monologue) for monologue in json.get("monologues", [])]
        )

class Monologue:
    def __init__(self, speaker, elements):
        self.speaker = speaker
        self.elements = elements

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls(
            json["speaker"],
            [Element.from_json(element) for element in json.get("elements", [])]
        )

class Element:
    def __init__(self, type_, value, timestamp, end_timestamp, confidence):
        self.type_ = type_
        self.value = value
        self.timestamp = timestamp
        self.end_timestamp = end_timestamp
        self.confidence = confidence

    @classmethod
    def from_json(cls, json):
        """Alternate constructor used for parsing json"""
        return cls(
            json["type"],
            json["value"],
            json.get("ts"),
            json.get("end_ts"),
            json.get("confidence")
        )

