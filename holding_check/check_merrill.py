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
        date_value = row['Trade Date']
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

# For each divident, find the purchase with the greatest date that is
# <= the divident date.  Also find the sale with the smallest date
# that is >= the dividend date.
table_data: Dict[str, List[Any]] = collections.defaultdict(list)
for _, row in combined_table.iterrows():
    trans_type = row['trans_type']
    if trans_type == 'Dividend':
        div_date = row['date']
        div_company = row['company']
        greatest_purchase: Optional[datetime.datetime] = None
        least_sale: Optional[datetime.datetime] = None
        for _skip, check_row in combined_table.iterrows():
            if check_row['company'] != div_company:
                continue
            if check_row['trans_type'] == 'Purchase':
                if check_row['date'] <= div_date:
                    if greatest_purchase is None:
                        greatest_purchase = check_row['date']
                    else:
                        greatest_purchase = max(greatest_purchase,
                                                check_row['date'])
            elif check_row['trans_type'] == 'Sale':
                if check_row['date'] >= div_date:
                    if least_sale is None:
                        least_sale = check_row['date']
                    else:
                        least_sale = min(least_sale, check_row['date'])
        if greatest_purchase is None:
            greatest_purchase = datetime.datetime(year=2025, month=1, day=1)
        if least_sale is None:
            least_sale = datetime.datetime(year=2025, month=12, day=31)
        duration = least_sale - greatest_purchase
        duration_days = (duration.total_seconds() / 60. / 60. / 24.)
        table_data['company'].append(div_company)
        table_data['amount'].append(row['amount'])
        table_data['duration_days'].append(duration_days)
        table_data['purchase'].append(greatest_purchase)
        table_data['sale'].append(least_sale)
        table_data['div date'].append(div_date)

qualified_table = pd.DataFrame(table_data)
qualified_table.sort_values('duration_days', inplace=True)
print(qualified_table)
print('unqualified')
print(qualified_table[qualified_table['duration_days'] < 60])
unqual_table = qualified_table[qualified_table['duration_days'] < 60].copy()
total_unqual = 0.
for _, row in unqual_table.iterrows():
    total_unqual += row['amount']
print('total unqual', total_unqual)

unqual_table.to_excel(data_folder / 'short_holding_period.xlsx')
