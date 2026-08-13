import collections
import datetime
import json
import pathlib
import re
from typing import Any, List, Dict

import pandas as pd  # type: ignore

data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'finance' /
               'retirement')
tax_json_file = data_folder / 'tax_estimation_2026.json'

rmd_factor_file = data_folder / 'rmd_table.csv'
rmd_data_file = data_folder / 'rmd_computation_2026.json'


def mainprog() -> None:
    rmd_factor_table = pd.read_csv(rmd_factor_file)
    print('rmd factors')
    print(rmd_factor_table)
    with open(rmd_data_file, 'r') as load_file:
        rmd_data = json.load(load_file)
    for key in ('current_date', ):
        rmd_data[key] = datetime.datetime.fromisoformat(rmd_data[key])
    print(rmd_data)


mainprog()
