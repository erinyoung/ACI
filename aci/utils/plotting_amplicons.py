#!/usr/bin/env python

"""Graphs the dataframe"""

import logging

from .plotting_boxplot import plotting_boxplot


def plotting_amplicons(df, min_df, out):
    """graphs the dataframe"""

    # writing results to a file
    df.to_csv(f"{out}/amplicon_depth.csv", index=False)
    min_df.to_csv(f"{out}/amplicon_min_depth.csv", index=False)

    # getting rid of column with all the bam names
    df = df.drop("bam", axis=1)
    min_df = min_df.drop("bam", axis=1).astype(float)

    df = df.astype(float)
    min_df = min_df.astype(float)
    logging.debug(df)

    d = {
        "title": "Primer Assessment",
        "ylabel": "mean depth",
        "xlabel": "amplicon name",
        "file": f"{out}/amplicon_depth.png",
    }

    plotting_boxplot(df, d)

    min_d = {
        "title": "Primer Assessment",
        "ylabel": "mean depth",
        "xlabel": "amplicon name",
        "file": f"{out}/amplicon_min_depth.png",
    }

    plotting_boxplot(min_df, min_d)
