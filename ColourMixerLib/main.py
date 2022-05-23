from ColourMixerLib.utils import parse_arguments, read_from_file
from ColourMixerLib.Color import Color

import warnings


def mix_colors(colors: list['Color']) -> 'Color':
    return sum(colors)/len(colors)


def lowest_color(colors: list['Color']) -> 'Color':
    temp_color = Color(255, 255, 255, 255)
    for c in colors:
        temp_color = temp_color.lower(c)
    return temp_color


def highest_color(colors: list['Color']) -> 'Color':
    temp_color = Color(255, 255, 255, 255)
    for c in colors:
        temp_color = temp_color.higher(c)
    return temp_color


def hsl_mix_colors(colors: list['Color']) -> 'Color':
    def mean(arr):
        return sum(arr)/len(arr)
    hsl = tuple(mean(z) for z in zip(*[c.to_hsl().values() for c in colors]))
    return Color.from_hsl(hsl)


def get_result() -> 'Color':
    cli = parse_arguments()

    mode, raw_colors_cli, raw_colors_f = cli['mode'], cli['raw_colors'], read_from_file()

    colors_f = [Color.from_str(s) for s in raw_colors_f if Color.from_str(s)]
    colors_cli = [Color.from_str(s) for s in raw_colors_cli if Color.from_str(s)]

    colors = colors_cli + colors_f
    if not colors:
        raise ValueError('zero valid colors given')

    if mode not in ['mix', "lowest", "highest", "mix-saturate"]:
        warnings.warn(f"'{mode}' isn't a valid mode, proceeding with default 'mix'", SyntaxWarning, stacklevel=2)
        mode = 'mix'

    match mode:
        case 'mix':
            return mix_colors(colors)
        case 'lowest':
            return lowest_color(colors)
        case 'highest':
            return highest_color(colors)
        case 'mix-saturate':
            return hsl_mix_colors(colors)
        case _:
            raise SyntaxError('invalid mode')
