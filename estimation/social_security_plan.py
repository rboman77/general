import collections
import pathlib
import datetime

import pandas as pd  # type: ignore

data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'finance' /
               'retirement')
input_sheet = data_folder / 'social_security_dates.xlsx'
output_sheet = data_folder / 'social_security_balances.xlsx'


def mainprog():
    sheet_table = pd.read_excel(input_sheet)
    table_data = collections.defaultdict(list)
    print(sheet_table)
    for _, row in sheet_table.iterrows():
        balance = row['assets']
        return_rate = row['return']
        start_date = row['compute_start_date'].to_pydatetime()
        his_start_date = row['his_start_date'].to_pydatetime()
        her_start_date = row['her_start_date'].to_pydatetime()
        current_date = start_date
        num_months = 12 * row['years']
        for i in range(num_months):
            print(i, current_date)
            withdraw = 10000
            if current_date >= his_start_date:
                withdraw -= row['his_monthly']
            if current_date >= her_start_date:
                withdraw -= 0.5 * row['his_monthly']
            current_date += datetime.timedelta(days=30)
            balance -= withdraw
            balance += 30. / 365. * return_rate * balance
            table_data['label'].append(row['label'])
            table_data['date'].append(current_date)
            table_data['withdraw'].append(withdraw)
            table_data['balance'].append(balance)
        # start_time = datetime.datetime(row['compute_start_date'])
        # print('start time', start_time)
    table = pd.DataFrame(table_data)
    table.to_excel(output_sheet)


mainprog()
