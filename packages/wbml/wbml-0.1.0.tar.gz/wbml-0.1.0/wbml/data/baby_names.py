# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import pandas as pd

from .data import data_path

__all__ = ['load']


def load():
    data = pd.read_csv(data_path('baby_names', 'names.csv'))

    # Fix index and move outputs to columns.
    data = data.set_index(['name', 'gender']).T

    # Convert indices to ints.
    data.index = map(int, data.index)

    return data
