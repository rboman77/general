import collections
import json
import pathlib
from typing import Any, List, Dict

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


def mainprog() -> None:
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

    # Add total income and capital gains.
    total_income = 0
    for label, entry in tax_data['normal_income']:
        total_income += entry
    print('total income', total_income)

    total_capital_gains = 0
    for label, entry in tax_data['capital_gains']:
        total_capital_gains += entry

    print('total capital gains', total_capital_gains)

    irs_tax = tax_from_brackets(
        tax_data['irs_brackets'],
        total_income - tax_data['irs_standard_deduction'])
    california_tax = tax_from_brackets(
        tax_data['california_brackets'],
        total_income - tax_data['california_standard_deduction'])

    irs_total_paid = 0
    for label, entry in tax_data['irs_payments']:
        irs_total_paid += entry

    california_total_paid = 0
    for label, entry in tax_data['california_payments']:
        california_total_paid += entry

    table_data: Dict[str, Any] = collections.defaultdict(list)

    table_data['account'].append('irs')
    table_data['total_tax'].append(irs_tax)
    table_data['paid'].append(irs_total_paid)
    table_data['balance'].append(irs_tax - irs_total_paid)

    table_data['account'].append('CA')
    table_data['total_tax'].append(california_tax)
    table_data['paid'].append(california_total_paid)
    table_data['balance'].append(california_tax - california_total_paid)

    table = pd.DataFrame(table_data)
    print(table)


mainprog()
