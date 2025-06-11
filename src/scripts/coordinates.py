from dataclasses import dataclass


@dataclass
class Dimension:
    width: float
    height: float

    def scale_by(self, x: float, y: float):
        self.x *= x
        self.y *= y


@dataclass
class Position:
    x: float
    y: float

    def __post_init__(self):
        assert 0 <= self.x <= 1, "X coordinate must be between 0 and 1"
        assert 0 <= self.y <= 1, "Y coordinate must be between 0 and 1"

    def scale_by(self, x: float, y: float):
        self.x *= x
        self.y *= y

    def translate_by(self, x: float, y: float):
        self.x += x
        self.y += y
