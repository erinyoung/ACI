#!/usr/bin/env python

""" Getting coverage ready for plotting """

import logging

from .split_dataframe   import split_dataframe
from .plotting_boxplot  import plotting_boxplot

def plotting_depth(df, out):
    """ Getting coverage ready for plotting """

    df = split_dataframe(df)

    # writing results to a file
    df.to_csv(out + '/overall_depth.csv', index=False)

    # restructuring for boxplot
    df['ungroup'] = df['group'] * 500
    df = df.drop('pos', axis=1)
    df = df.drop('group', axis=1)
    df = df.set_index('ungroup')
    df = df.transpose()

    logging.debug('Restructured coverage boxplot')
    logging.debug(df)

    d = {
        'title' : 'Overall coverage',
        'ylabel' : 'meandepth',
        'xlabel' : 'position',
        'file' : out + '/overall_depth.png'
    }

    plotting_boxplot(df,d)
