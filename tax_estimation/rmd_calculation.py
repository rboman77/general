import collections
import json
import pathlib
import re
from typing import Any, List, Dict

import pandas as pd  # type: ignore

data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'finance' /
               'retirement')
tax_json_file = data_folder / 'tax_estimation_2026.json'

rmd_factor_file = data_folder / 'rmd_table.csv'


def mainprog() -> None:
    rmd_factor_table = pd.read_csv(rmd_factor_file)
    print(rmd_factor_table)


mainprog()
