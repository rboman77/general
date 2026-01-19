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
    """Load a CSV file and return as a dataframe. Convert numbers in
    parens to negative values.  Parse dates."""
    raw_table = pd.read_csv(file_path)
    return raw_table


for csv_file in data_folder.glob('*.csv'):
    print(csv_file)
