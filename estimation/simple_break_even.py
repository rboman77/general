import collections
import json
import pathlib
from typing import Any, Dict, List

import pandas as pd

data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'finance' /
               'retirement')
json_file = data_folder / 'ss_break_even.json'
with open(json_file, 'r') as load_file:
    ss_data = json.load(load_file)


def main_prog() -> None:
    start_pay = ss_data['feb 2026']
    start_age = ss_data['start age']
    return_rate = 0.05
    print(start_pay, start_age)
    start_pay_delayed = start_pay * 1.08
    table_data: Dict[str, List[Any]] = collections.defaultdict(list)
    table_data['year'].append(2026)
    table_data['age'].append(start_age)
    table_data['ss_pay_no_wait'].append(start_pay)
    table_data['ss_pay_wait'].append(0)
    for i in range(30):
        table_data['year'].append(2027 + i)
        table_data['age'].append(start_age + i)
        table_data['ss_pay_no_wait'].append(
            (start_pay * (1 + return_rate)) * (1 + i))
        table_data['ss_pay_wait'].append(start_pay_delayed * i)
    table = pd.DataFrame(table_data)
    print(table)


main_prog()
