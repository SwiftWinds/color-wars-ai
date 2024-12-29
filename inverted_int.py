class InvertedInt:
    def __init__(self, value: int):
        self.value = value

    def __str__(self):
        return f"1/{self.value}"

    def __repr__(self):
        return f"InvertedInt({self.value})"

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return (
            self.value > other.value
            if self.value ^ other.value >= 0
            else self.value < other.value
        )

    def __ge__(self, other):
        return not self < other

    def __neg__(self):
        return InvertedInt(-self.value)