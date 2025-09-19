import collections
import pathlib
import datetime

import pandas as pd  # type: ignore

data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'finance' /
               'retirement')
input_sheet = data_folder / 'social_security_dates.xlsx'


def mainprog():
    sheet_table = pd.read_excel(input_sheet)
    print(sheet_table)
    for _, row in sheet_table.iterrows():
        table_data = collections.defaultdict(list)
        start_time = row['compute_start_date'].to_pydatetime()
        current_time = start_time
        num_months = 12 * row['years']
        for i in range(num_months):
            print(i, current_time)
            current_time += datetime.timedelta(days=30)
        # start_time = datetime.datetime(row['compute_start_date'])
        # print('start time', start_time)


mainprog()
