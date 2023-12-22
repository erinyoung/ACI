#!/usr/bin/env python

""" Takes a bam file and sorts and indexes it with pysam """

import os
import pysam

def prep(meta, threads):
    """ Sorts and indexes bam files listed in dic """

    if os.path.exists(bam0):
        pysam.sort('-o', bam1, '-@', str(threads), bam0)

    if os.path.exists(bam1):
        pysam.index(bam1)
