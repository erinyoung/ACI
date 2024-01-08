#!/usr/bin/env python

""" Gets mean for each group """

import numpy as np

def group_mean(df, name):
    """ Gets mean for each group """
    df_name = df[df['bam'] == name].copy()
    df_name['group'] = (df_name['pos'] / 500).apply(np.floor)
    df_name = df_name[['group', 'cov']]
    df_name.columns = ['group', name]
    df_name = df_name.groupby(['group']).mean().reset_index()
    return df_name
