from typing import NamedTuple
from colorsys import rgb_to_hls, hls_to_rgb
import re


class Color(NamedTuple):
    red:    int
    green:  int
    blue:   int
    alpha:  int = 255

    def __add__(self, other) -> 'Color':
        return Color(self.red + other.red, self.green + other.green, self.blue + other.blue, self.alpha + other.alpha)

    def __radd__(self, other) -> 'Color':
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __floordiv__(self, other) -> 'Color':
        return Color(self.red // other, self.green // other, self.blue // other, self.alpha // other)

    def __truediv__(self, other) -> 'Color':
        return self.__floordiv__(other)

    @staticmethod
    def dec_match(number: str) -> bool:
        if bool(re.match(r'^((\d{1,3},){3}\d{1,3})$', number)):
            return all(int(i) <= 255 for i in number.split(','))
        return False

    @staticmethod
    def hex_match(number: str) -> bool:
        return bool(re.match(r'^([\da-f]{3}|[\da-f]{6}|[\da-f]{8})$', number))

    @classmethod
    def from_hex(cls, h: str) -> 'Color':
        match len(h):
            case 3:
                return cls(*[int(n, 16) for n in list(h)])
            case 6 | 8:
                return cls(*[int(n, 16) for n in re.findall(r'..', h)])
            case _:
                raise ValueError(f"number {h} is invalid")

    @classmethod
    def from_rgb(cls, rbg: str) -> 'Color':
        return cls(*[int(n) for n in rbg.split(',')])

    @classmethod
    def from_str(cls, s: str) -> 'Color':
        if Color.hex_match(s):
            return Color.from_hex(s)
        elif Color.dec_match(s):
            return Color.from_rgb(s)

    @classmethod
    def from_hsl(cls, hsl: tuple | dict[str, float]) -> 'Color':
        match hsl:
            case tuple():
                h, s, l = hsl
                return cls(*[round(c * 255) for c in hls_to_rgb(h / 360, l, s)])
            case dict():
                return cls(*[round(c * 255) for c in hls_to_rgb(hsl['h'] / 360, hsl['l'], hsl['s'])])
            case _:
                raise TypeError("unsupported type")

    def to_hex(self) -> str:
        return f"#{self.red:02x}{self.green:02x}{self.blue:02x}{self.alpha:02x}"

    def to_hsl(self) -> dict[str, float]:
        r = self.red / 255
        g = self.green / 255
        b = self.blue / 255
        hue, lightness, saturation = rgb_to_hls(r, g, b)
        return {'h': hue * 360, 's': saturation, 'l': lightness}

    def lower(self, c: 'Color') -> 'Color':
        return Color(min(self.red, c.red), min(self.green, c.green), min(self.blue, c.blue), min(self.alpha, c.alpha))

    def higher(self, c: 'Color') -> 'Color':
        return Color(max(self.red, c.red), max(self.green, c.green), max(self.blue, c.blue), max(self.alpha, c.alpha))

    def describe(self) -> None:
        hsl = self.to_hsl()
        print(f"Red: {self.red}, Green: {self.green}, Blue: {self.blue}, Alpha: {self.alpha}\n"
              f"Hex: {self.to_hex()}, Hue: {hsl['h']:.0f}, Saturation: {hsl['s']:.3g}, Lightness: {hsl['l']:.3g}")
