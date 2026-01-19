import collections
import datetime
import json
import pathlib
import re
from typing import Any, List, Dict, Optional, Set

import pandas as pd  # type: ignore

data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'finance' /
               'holding_period_2025')


def to_num_strip_commas(input_str: str) -> float:
    return float(re.sub(',', '', input_str))


def extract_paren_value(str_num: str) -> float:
    m = re.search('\\(([^)]+)\\)', str_num)
    if m:
        return -to_num_strip_commas(m.group(1))
    return to_num_strip_commas(str_num)


def load_file(file_path: pathlib.Path) -> pd.DataFrame:
    """Load a CSV file and return as a dataframe. Convert numbers in
    parens to negative values.  Parse dates."""

    # Trade Date
    # Settlement Date
    # Pending/Settled
    # Account Nickname
    # Account Registration
    # Account #
    # Type
    # Description 1
    # Description 2
    # Symbol/CUSIP #
    # Quantity
    # Price ($)
    # Amount ($)

    # Date format: 3/31/2025
    raw_table = pd.read_csv(file_path)
    table_data: Dict[str, List[Any]] = collections.defaultdict(list)
    for _, row in raw_table.iterrows():
        date_value = row['Settlement Date']
        decoded_date = datetime.datetime.strptime(date_value, '%m/%d/%Y')
        table_data['date'].append(decoded_date)
        table_data['amount'].append(extract_paren_value(row['Amount ($)']))
        # for key in ('Type', 'Description 1 ', 'Description 2'):
        #    table_data[key].append(row[key])
        table_data['trans_type'].append(row['Description 1 '].strip())
        table_data['company'].append(row['Symbol/CUSIP #'])
    return pd.DataFrame(table_data)


combined_table: Optional[pd.DataFrame] = None
for csv_file in data_folder.glob('*.csv'):
    loaded_table = load_file(csv_file)
    if combined_table is None:
        combined_table = loaded_table
    else:
        combined_table = pd.concat((combined_table, loaded_table))
assert combined_table is not None
print(min(combined_table['date']), max(combined_table['date']))
print('entries:', len(combined_table.index))
print(combined_table)

# Check to see if any company had a purchase, sale, and dividend in the year.
trans_set: Dict[str, Set[str]] = collections.defaultdict(set)
for _, row in combined_table.iterrows():
    trans_type = row['trans_type']
    if trans_type in ('Purchase', 'Sale', 'Dividend'):
        trans_set[row['company']].add(trans_type)

for key, value in trans_set.items():
    if len(value) == 3:
        print(key, value)
