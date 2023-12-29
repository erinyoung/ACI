#!/usr/bin/env python

""" Gets column names in order """

import logging
import pandas as pd

def column_names(bed):
    """ Takes a bed file, sorts it, and gets column names """

    df = pd.read_table(bed, header=None)
    df = df.sort_values([1, 2], ascending=[True, True])

    if len(df.columns) < 4:
        df[3] = df.index

    df[3] = df[3].astype(str)
    names = df[3].tolist()

    logging.debug("Names of amplicons :")
    logging.debug(names)

    return names
