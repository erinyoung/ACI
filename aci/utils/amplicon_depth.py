#!/usr/bin/env python

""" Use pysam to get depth for amplicon region """

import os
import pysam
from . import subregion, within, without

def amplicon_depth(df, bam, out, region):
    """ Use pysam to get depth for amplicon region """

    # setting default value
    cov       = 0

    # naming temporary files
    # pylint was complaining about too many variables
    # file_name = os.path.basename(bam)
    # name      = region.split(':')[3]
    bam0      = out + '/tmp.' + os.path.basename(bam)
    bam1      = out + '/tmp.' + region.split(':')[3] + '.1.' + os.path.basename(bam)
    bam2      = out + '/tmp.' + region.split(':')[3] + '.2.' + os.path.basename(bam)
    bam3      = out + '/tmp.' + region.split(':')[3] + '.3.' + os.path.basename(bam)
    bam4      = out + '/tmp.' + region.split(':')[3] + '.4.' + os.path.basename(bam)
    bed       = out + '/tmp.' + region.split(':')[3] + '.' + os.path.basename(bam) + '.bed'

    # getting subregion information and creating bedfile
    subrange  = subregion(region, bed) # pylint: disable=E1102

    # reduce bam file to something smaller
    if os.path.exists(bam0):
        within(bam0, bam1, subrange) # pylint: disable=E1102

    if os.path.exists(bam1):
        pysam.index(bam1)

        # remove all reads that fall outside of region of interest
        without(bam1, bam2, bam3, subrange) # pylint: disable=E1102

    if os.path.exists(bam2):
        pysam.index(bam2)

        # get only reads that are within subrange
        within(bam2, bam4, subrange) # pylint: disable=E1102

    if os.path.exists(bam4):
        pysam.index(bam4)

        # get the coverage of the region (finally!)
        cov = float(pysam.coverage('--no-header', bam4, '-r', subrange).split()[6])

    # removing files
    tmpfiles = [bed, bam1, bam2, bam3, bam4]
    for file in tmpfiles:
        if os.path.exists(file):
            os.remove(file)
        if os.path.exists(file + '.bai'):
            os.remove(file + '.bai')

    bamindex = df.index[df['bam'] == bam]
    df.loc[bamindex, [region.split(':')[3]]] = cov
