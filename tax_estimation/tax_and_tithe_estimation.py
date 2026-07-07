import collections
import json
import pathlib
import re
from typing import Any, List, Dict

import pandas as pd  # type: ignore

data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'finance' /
               'retirement')
tax_json_file = data_folder / 'tax_estimation_2026.json'


def tax_from_brackets(brack_list, amount, bracket_offset=0.):
    # Sanity check on brackets.
    for i in range(len(brack_list) - 1):
        assert brack_list[i]["high"] == brack_list[i + 1]["low"]
        assert brack_list[i]["low"] < brack_list[i + 1]["low"]
        assert brack_list[i]["high"] < brack_list[i + 1]["high"]

    result = 0.
    for brack in brack_list:
        if amount > (brack["low"] + bracket_offset) and amount >= (
                brack["high"] + bracket_offset):
            result += brack["rate"] * (brack["high"] - brack["low"])
        elif amount > (brack["low"] + bracket_offset) and amount < (
                brack["high"] + bracket_offset):
            result += brack["rate"] * (amount -
                                       (brack["low"] + bracket_offset))
        elif amount >= brack["high"] + bracket_offset:
            pass
        elif amount <= brack["low"] + bracket_offset:
            pass
        else:
            assert False
        # print('after brack', brack, amount, result)
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

    normal_inc_before_ded = total_income
    irs_tax = tax_from_brackets(
        tax_data['irs_brackets'],
        total_income - tax_data['irs_standard_deduction'])

    capital_gain_tax = tax_from_brackets(tax_data['irs_capital_gain_brackets'],
                                         total_capital_gains)

    social_security_income = 0
    for label, entry in tax_data['normal_income']:
        if re.search('^social security', label, re.IGNORECASE):
            social_security_income += entry

    california_tax = tax_from_brackets(
        tax_data['california_brackets'], total_income + total_capital_gains -
        -social_security_income - tax_data['california_standard_deduction'])

    irs_total_paid = 0
    for label, entry in tax_data['irs_payments']:
        irs_total_paid += entry

    california_total_paid = 0
    for label, entry in tax_data['california_payments']:
        california_total_paid += entry

    table_data: Dict[str, Any] = collections.defaultdict(list)

    table_data['account'].append('irs')
    table_data['total_tax'].append(irs_tax + capital_gain_tax)
    table_data['paid'].append(irs_total_paid)
    table_data['balance'].append(irs_tax - irs_total_paid)

    table_data['account'].append('CA')
    table_data['total_tax'].append(california_tax)
    table_data['paid'].append(california_total_paid)
    table_data['balance'].append(california_tax - california_total_paid)

    tithe_income = 0
    for label, entry in tax_data['normal_income']:
        tithe_income += entry
    for label, entry in tax_data['capital_gains']:
        tithe_income += entry

    tithe_payment = 0
    for label, entry in tax_data['tithe_payments']:
        tithe_payment += entry

    table_data['account'].append('tithe')
    table_data['total_tax'].append(tithe_income / 10.)
    table_data['paid'].append(tithe_payment)
    table_data['balance'].append(tithe_income / 10. - tithe_payment)

    table_data['account'].append('normal income before ded')
    table_data['total_tax'].append(0)
    table_data['paid'].append(normal_inc_before_ded)
    table_data['balance'].append(0)

    table_data['account'].append('capital gains')
    table_data['total_tax'].append(0)
    table_data['paid'].append(total_capital_gains)
    table_data['balance'].append(0)

    table_data['account'].append('social security payments')
    table_data['total_tax'].append(0)
    table_data['paid'].append(social_security_income)
    table_data['balance'].append(0)

    table = pd.DataFrame(table_data)
    print(table)
    table.to_excel(data_folder / 'estimated_tax_15_jan_2026.xlsx')


mainprog()
