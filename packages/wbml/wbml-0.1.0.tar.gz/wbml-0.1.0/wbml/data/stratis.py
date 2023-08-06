# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import os
import re
from collections import OrderedDict

import netCDF4 as nc
import numpy as np
import pandas as pd

from .data import data_path

__all__ = ['load']


def load():
    # Load observations.
    data = nc.Dataset(data_path('stratis', 'erai_T2_1979-2016_daily.nc'))
    matrix = data['T2'][:].reshape(data['T2'].shape[0], -1)
    obs = pd.DataFrame(matrix, index=pd.Index(data['time'][:], name='time'))

    # Load locations.
    lat = data['latitude'][:]
    lon = data['longitude'][:]
    lat, lon = np.broadcast_arrays(lat[:, None], lon[None, :])
    assert lat.shape == data['T2'].shape[1:3]
    loc = pd.DataFrame({'latitude': lat.flatten(),
                        'longitude': lon.flatten()})

    # Find simulator files.
    sim_files = os.listdir(data_path('stratis'))
    sim_files = [f for f in sim_files
                 if os.path.splitext(f)[1].lower() == '.nc'
                 if f != 'erai_T2_1979-2016_daily.nc']

    # Load olmm.
    sims = OrderedDict()
    for sim_file in sim_files:
        data = nc.Dataset(data_path('stratis', sim_file))
        matrix = data['tas'][:].reshape(data['tas'].shape[0], -1)
        sim_name = re.match(r'^cmip5_tas_amip_(.*)_r1i1p1_1979-2008.nc$',
                            sim_file).group(1)
        sims[sim_name] = \
            pd.DataFrame(matrix, index=pd.Index(data['time'][:], name='time'))

    return loc, obs, sims
