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
dist_period_key = 'Distribution Period'


def mainprog() -> None:
    rmd_factor_table = pd.read_csv(rmd_factor_file)
    # print('rmd factors')
    # print(rmd_factor_table)
    with open(rmd_data_file, 'r') as load_file:
        rmd_data = json.load(load_file)
    for key in ('current_date', ):
        rmd_data[key] = datetime.datetime.fromisoformat(rmd_data[key])
    # print(rmd_data)

    years_to_wait = 73 - rmd_data['current_age']
    print('years to wait', years_to_wait)
    print('current balance', rmd_data['current_value'])
    adjusted_balance = rmd_data['current_value'] * (rmd_data['growth_rate']**
                                                    years_to_wait)
    print('adjusted balance', adjusted_balance)
    for i in range(30):
        age = i + rmd_data['current_age']
        if age < 73:
            continue
        sub_table = rmd_factor_table[rmd_factor_table['Age'] == age]
        assert len(sub_table.index) == 1
        age_factor = sub_table.iloc[0][dist_period_key]
        print(i, age, age_factor)

    # For each year:
    #    Use the table for this age and get the RMD.
    #    Reduce the balance by this amount.
    #    Increase the balance by the increase factor.


mainprog()
