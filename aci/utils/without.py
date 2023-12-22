#!/usr/bin/env python

""" Takes a bam file and maps those within and without a region specified by a bedfile """

import os
import pysam

def without(bam0, bam1, bam2, bed):
    """ splits reads to those within (bam2) and without (bam1) subregion """

    if os.path.exists(bam0):
        pysam.index(bam1)
        pysam.view('-bh', bam0, '-U', bam1, '-o', bam2, '-L', bed, catch_stdout=False)
