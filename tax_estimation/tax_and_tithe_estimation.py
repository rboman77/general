import json
import pathlib

import pandas as pd  # type: ignore

data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'finance' /
               'retirement')
tax_json_file = data_folder / 'tax_estimation_2025.json'


def tax_from_brackets(brack, amount):
    # First check brackets for consistency.
    for i in range(len(brack) - 1):
        assert brack[i]["high"] == brack[i + 1]["low"]
        assert brack[i]["low"] < brack[i + 1]["low"]
        assert brack[i]["high"] < brack[i + 1]["high"]
    return 0


def mainprog():
    with open(tax_json_file, 'r') as load_file:
        tax_data = json.load(load_file)
    print('checking irs brackets')
    tax_from_brackets(tax_data['irs_brackets'], 0.)
    print('checking ca brackets')
    tax_from_brackets(tax_data['california_brackets'], 0.)

    # Some test cases.


mainprog()
