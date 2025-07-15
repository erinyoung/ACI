#!/usr/bin/env python

"""Gets coverage for bam file"""

import logging
import pandas as pd
import os
import pysam


def genome_depth(bam):
    """Takes a bam file file and gets coverage"""

    # getting depth results from pysam
    df = pd.DataFrame(
        [x.split("\t") for x in pysam.depth(bam).split("\n")]
    )  # pylint: disable=E1101
    df.columns = ["ref", "pos", "cov"]

    # ensuring that the type is correct
    df["pos"] = pd.to_numeric(df["pos"], errors="coerce")
    df["cov"] = pd.to_numeric(df["cov"], errors="coerce")
    df["bam"] = os.path.basename(bam)
    df = df.dropna()

    logging.debug(f"pysam results for {os.path.basename(bam)}")  # pylint: disable=W1203
    logging.debug(df)

    return df
