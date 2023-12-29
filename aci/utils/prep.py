#!/usr/bin/env python

""" Takes a bam file and sorts and indexes it with pysam """

import os
import pysam

def prep(initial, final, threads):
    """ Sorts and indexes bam files listed in dic """

    if os.path.exists(initial):
        pysam.sort('-o', final, '-@', str(threads), initial)

    if os.path.exists(final):
        pysam.index(final)
