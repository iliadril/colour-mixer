import argparse
import os.path
import re


def initialize_parser() -> 'argparse.ArgumentParser':
    parser = argparse.ArgumentParser(
        prog='Colour mixer',
        description='A simple script to parse RGBA colors from CLI and .txt file',
        exit_on_error=True,
    )
    parser.add_argument('-m', '--mode',
                        action='store',
                        nargs='?',
                        const='mix',
                        default='mix',
                        dest='mode',
                        help='choose a mixing mode',
                        )
    return parser


def parse_arguments() -> dict[str, list[str]]:
    p = initialize_parser()
    args, colors = p.parse_known_args()
    return {'mode': args.mode, 'raw_colors': colors}


def read_from_file(path: str = os.path.join(os.getcwd(), 'colors.txt')) -> list[str]:
    with open(path, mode='r') as f:
        return [raw_colour.strip() for raw_colour in f]
