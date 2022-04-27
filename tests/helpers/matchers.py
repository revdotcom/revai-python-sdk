class Matcher:
    def __init__(self, condition):
        self.condition = condition

    def __eq__(self, other):
        return self.condition(other)
