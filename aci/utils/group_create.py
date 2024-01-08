#!/usr/bin/env python

""" Creates groups """

import pandas as pd
import numpy as np

def group_create(positions):
    """ Creates groups for later averaging """

    df = pd.DataFrame([])
    df['pos'] = positions
    df['group'] = (df['pos'] / 500).apply(np.floor)
    df = df.drop('pos', axis=1)
    df = df.drop_duplicates()

    df['start'] = (df['group'] * 500).astype(int)
    df['end']   = (df['group'] * 500 + 499).astype(int)
    df['pos']   = df['start'].astype('str') + '-' + df['end'].astype('str')

    return df[['pos', 'group']]
