#!/usr/bin/env python

""" Graphs the dataframe """

import logging

from .plotting_boxplot import plotting_boxplot

def plotting_amplicons(df, out):
    """ graphs the dataframe """

    # writing results to a file
    df.to_csv(out + '/amplicon_depth.csv', index=False)

    # getting rid of column with all the bam names
    df = df.drop('bam', axis=1)
    df = df.astype(float)
    logging.debug(df)

    d = {
        'title': 'Primer Assessment',
        'ylabel': 'mean depth',
        'xlabel' : 'amplicon name',
        'file' : out + '/amplicon_depth.png'
    }

    plotting_boxplot(df,d)
