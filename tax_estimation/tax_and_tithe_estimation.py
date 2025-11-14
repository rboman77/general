import json
import pathlib

import pandas as pd  # type: ignore

data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'finance' /
               'retirement')
tax_json_file = data_folder / 'tax_estimation_2025.json'


def mainprog():
    with open(tax_json_file, 'r') as load_file:
        tax_data = json.load(load_file)
    print(json.dumps(tax_data, indent=4))


mainprog()
