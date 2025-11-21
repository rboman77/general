import json
import pathlib

import pandas as pd  # type: ignore

data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'finance' /
               'retirement')
tax_json_file = data_folder / 'tax_estimation_2025.json'


def tax_from_brackets(brack_list, amount):
    # Sanity check on brackets.
    for i in range(len(brack_list) - 1):
        assert brack_list[i]["high"] == brack_list[i + 1]["low"]
        assert brack_list[i]["low"] < brack_list[i + 1]["low"]
        assert brack_list[i]["high"] < brack_list[i + 1]["high"]

    result = 0.
    for brack in brack_list:
        if amount > brack["low"] and amount >= brack["high"]:
            result += brack["rate"] * (brack["high"] - brack["low"])
        elif amount > brack["low"] and amount < brack["high"]:
            result += brack["rate"] * (amount - brack["low"])
        elif amount >= brack["high"]:
            pass
        elif amount <= brack["low"]:
            pass
        else:
            assert False
        print('after brack', brack, amount, result)
    return result


def mainprog():
    with open(tax_json_file, 'r') as load_file:
        tax_data = json.load(load_file)
    print('checking irs brackets')
    tax_from_brackets(tax_data['irs_brackets'], 0.)
    print('checking ca brackets')
    tax_from_brackets(tax_data['california_brackets'], 0.)

    # Some test cases.
    print('test 1')
    value = 23000.
    x = tax_from_brackets(tax_data['irs_brackets'], value)
    print('test', x, 'expecting', 0.1 * value)

    print('test 2')
    delta = 100.
    value = tax_data['irs_brackets'][0]['high'] + delta
    x = tax_from_brackets(tax_data['irs_brackets'], value)
    print('test', x, 'expecting',
          0.1 * tax_data['irs_brackets'][0]['high'] + 0.12 * delta)


mainprog()
