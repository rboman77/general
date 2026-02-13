import collections
import datetime
import json
import pathlib
import re
from typing import Any, List, Dict, Optional, Set

import pandas as pd  # type: ignore

data_folder = (pathlib.Path('/mnt') / 'g' / 'My Drive' / 'finance' /
               '2025_tax' / 'holding_period_2025_fidelity')
qualified_div_table = pd.read_csv(data_folder / 'qualified_div.csv')
qualified_div_table = qualified_div_table.fillna(0.)
sub_table = qualified_div_table[qualified_div_table['1b Qualified Dividends'] >
                                0]
sub_table = sub_table[['symbol', 'Date', '1b Qualified Dividends']].copy()
print(sub_table)
