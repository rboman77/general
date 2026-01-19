import collections
import json
import pathlib
import re
from typing import Any, List, Dict

import pandas as pd  # type: ignore

data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'finance' /
               'holding_period_2025')


def extract_paren_value(str_num: str) -> float:
    m = re.search('\\(([^)]+)\\)', str_num)
    if m:
        return -float(m.group(1))
    return float(str_num)


def load_file(file_path: pathlib.Path) -> pd.DataFrame:
    return pd.DataFrame({'x': [1]})


str_numbers = ('(100)', '200', '300', '(1.25)', '(25.1)', '77')

for x in str_numbers:
    print(x, extract_paren_value(x))
