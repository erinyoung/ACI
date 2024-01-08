#!/usr/bin/env python

""" Split datafame bam column into multiple columns """

import logging
import sys
import pandas as pd

from .group_create import group_create
from .group_mean import group_mean

def split_dataframe(df):
    """ Split datafame bam column into multiple columns """

    df['bam'] = df['bam'].astype(str)
    names     = df['bam'].tolist()
    names     = sorted(set(names))
    logging.debug('list of bams')
    logging.debug(names)

    df['pos'] = df['pos'].astype(int)
    positions = df['pos'].tolist()
    positions = sorted(set(positions))
    logging.debug('list of positions')
    logging.debug(positions)

    df['ref']  = df['ref'].astype(str)
    references = df['ref'].tolist()
    references = sorted(set(references))
    logging.debug('list of references')
    logging.debug(references)

    if len(references) > 1:
        logging.fatal('Bam files have more than one reference!')
        sys.exit(1)

    df_split = group_create(positions)

    logging.debug('The split dataframe is')
    logging.debug(df_split)

    for name in names:
        df_name = group_mean(df, name)
        df_split = pd.merge(df_split, df_name, left_on = 'group', right_on = 'group', how = 'outer')

    logging.debug('The split dataframe is')
    logging.debug(df_split)

    return df_split
