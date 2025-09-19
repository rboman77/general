import pathlib
import datetime

import pandas as pd  # type: ignore

sheet_path = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'finance' /
              'retirement' / 'social_security_dates.xlsx')


def mainprog():
    sheet_table = pd.read_excel(sheet_path)
    print(sheet_table)


mainprog()
