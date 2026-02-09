import collections
import json
import pathlib
from typing import Any, Dict, List

import pandas as pd
import holoviews as hv  # type: ignore

data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'finance' /
               'retirement')
json_file = data_folder / 'ss_break_even.json'
with open(json_file, 'r') as load_file:
    ss_data = json.load(load_file)


def main_prog() -> None:
    start_pay = ss_data['feb 2026']
    start_age = ss_data['start age']
    return_rate = 0.045
    print(start_pay, start_age)
    start_pay_delayed = start_pay * 1.08
    table_data: Dict[str, List[Any]] = collections.defaultdict(list)
    for i in range(35):
        table_data['year'].append(2026 + i)
        table_data['age'].append(start_age + i)
        table_data['no_wait'].append((start_pay * (1 + return_rate)) * (1 + i))
        if i >= 1:
            table_data['wait'].append(start_pay_delayed * i)
        else:
            table_data['wait'].append(0)

    table = pd.DataFrame(table_data)
    hv.extension('bokeh')
    plot_list = []
    for col_name in ('no_wait', 'wait'):
        plot = hv.Curve(table, kdims='age', vdims=col_name)
        plot_list.append(
            plot.opts(show_grid=True, width=800, height=800, tools=['hover']))

    plot = hv.Overlay(plot_list)
    hv.save(plot, data_folder / 'simple_break_even_plot.html')
    table.to_excel(data_folder / 'simple_break_even.xlsx')


main_prog()
