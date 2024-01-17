#!/usr/bin/env python
# pylint: disable=logging-fstring-interpolation

""" Use pysam to get depth for amplicon region """

import logging
import os
import pysam
from .subregion import subregion
from .within import within
from .without import without
from .get_coverage import get_coverage

def amplicon_depth(meta, region):
    """ Use pysam to get depth for amplicon region """

    # getting subregion information and creating bedfile
    subrange, name  = subregion(region)

    after_reduction_bam      = meta['tmp'] + name + '.step1.' + meta['file_name']
    removing_outside_matches = meta['tmp'] + name + '.step2.' + meta['file_name']
    junk_bam                 = meta['tmp'] + name + '.step3.' + meta['file_name']
    final_bam                = meta['tmp'] + name + '.step4.' + meta['file_name']
    logging.debug('The filenames are going to be :')
    logging.debug(meta)

    # setting the default value
    cov = 0.0

    # reduce bam file to something smaller
    if os.path.exists(meta['sorted_bam']):
        logging.debug(f"Step 1. reducing bam for speed for {meta['sorted_bam']}")
        within(meta['sorted_bam'], after_reduction_bam, subrange)

    if os.path.exists(after_reduction_bam):
        pysam.index(after_reduction_bam)

        # remove all reads that fall outside of region of interest
        # warning : this is the slow part of the script
        logging.debug(f"Step 2. reducing bam for speed for {meta['sorted_bam']}")
        without(after_reduction_bam,
                removing_outside_matches,
                junk_bam,
                bed = meta['tmp'] + name + '.bed')

    if os.path.exists(removing_outside_matches):
        pysam.index(removing_outside_matches)

        # get only reads that are within subrange
        logging.debug(f"Step 3. final reduction for {meta['sorted_bam']}")
        within(removing_outside_matches, final_bam, subrange)

    if os.path.exists(final_bam):
        pysam.index(final_bam)
        cov = get_coverage(final_bam, subrange)

    logging.info(f"Amplicon bam file created for {meta['file_name']} over {subrange}")

    return [meta['file_name'], name, cov]
