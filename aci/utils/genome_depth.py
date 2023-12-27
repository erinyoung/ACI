#!/usr/bin/env python

""" Gets coverage for bam file """

import pandas as pd
import pysam
import logging

def genome_depth(meta):
    """ Takes a bam file file and gets coverage """

    # getting depth results from pysam
    df = pd.DataFrame([x.split('\t') for x in pysam.depth(meta['sorted_bam']).split('\n')])
    df.columns = ['ref', 'pos', 'cov']

    # ensuring that the type is correct
    df['pos'] = pd.to_numeric(df['pos'], errors='coerce')
    df['cov'] = pd.to_numeric(df['cov'], errors='coerce')
    df['bam'] = meta['file_name']
    df = df.dropna()

    logging.debug('pysam results for ' + meta['sorted_bam'])
    logging.debug(df)

    return df
