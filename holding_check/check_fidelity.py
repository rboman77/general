import collections
import datetime
import json
import pathlib
import re
from typing import Any, List, Dict, Optional, Set

import pandas as pd  # type: ignore

data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'finance' /
               '2025_tax' / 'holding_period_2025_fidelity')


def read_csv_file(file_path) -> pd.DataFrame:
    result = pd.read_csv(file_path)
    result = result.fillna(0)
    if 'Date' not in result.columns:
        result['Date'] = result['Run Date']
    date_list = []
    for _, row in result.iterrows():
        if re.search('[0-9]{2}/[0-9]{2}/[0-9]{2}$', row['Date']):
            date_format = '%m/%d/%y'
        else:
            date_format = '%m/%d/%Y'
        date_list.append(
            datetime.datetime.strptime(row['Date'].strip(), date_format))
    result['Date'] = date_list
    return result


qualified_div_table = read_csv_file(data_folder / 'qualified_div.csv')
sub_table = qualified_div_table[qualified_div_table['1b Qualified Dividends'] >
                                0]
sub_table = sub_table[['symbol', 'Date', '1b Qualified Dividends']].copy()
print(sub_table)
for _, row in sub_table.iterrows():
    print(type(row['Date']))

trans_table = read_csv_file(data_folder / 'History_for_Account_Z24652142 .csv')
print(trans_table)

sub_table.to_excel(data_folder / 'processed_qualified_div.xlsx')
trans_table.to_excel(data_folder / 'processed_transactions.xlsx')
