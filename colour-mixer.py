#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")
elif sys.version_info[1] < 10:
    raise Exception("Must be using at least Python 3.10")

from ColourMixerLib.main import get_result

if __name__ == '__main__':
    final_color = get_result()
    final_color.describe()
