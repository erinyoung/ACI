#!/usr/bin/env python

""" Takes a bam file and maps those within and without a region specified by a bedfile """

import pysam

def without(initial, unmatched, matched, bed):
    """ splits reads to those within (bam2) and without (bam1) subregion """

    pysam.view('-bh', initial, '-U', unmatched, '-o', matched, '-L', bed, catch_stdout=False) # pylint: disable=E1101
