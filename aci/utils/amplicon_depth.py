#!/usr/bin/env python

""" Use pysam to get depth for amplicon region """

import logging
import os
import pysam
from .subregion import subregion
from .within import within
from .without import without

def amplicon_depth(meta, region):
    """ Use pysam to get depth for amplicon region """

    name = region.split(':')[3]

    # pylint was complaining about the number of variables
    # so they're all dict values instead
    meta['after_reduction_bam']      = meta['tmp'] + name + '.1.' + meta['file_name']
    meta['removing_outside_matches'] = meta['tmp'] + name + '.2.' + meta['file_name']
    meta['junk_bam']                 = meta['tmp'] + name + '.3.' + meta['file_name']
    meta['final_bam']                = meta['tmp'] + name + '.4.' + meta['file_name']
    meta['subregion_bed']            = meta['tmp'] + name + '.'   + meta['file_name'] + '.bed' # pylint: disable=C0301
    logging.debug('The filenames are going to be :')
    logging.debug(meta)

    # getting subregion information and creating bedfile
    subrange  = subregion(region, meta['subregion_bed'])

    # reduce bam file to something smaller
    if os.path.exists(meta['sorted_bam']):
        logging.debug('Step 1. reducing bam for speed for ' + meta['sorted_bam']) # pylint: disable=W1201
        within(meta['sorted_bam'], meta['after_reduction_bam'], subrange)

    if os.path.exists(meta['after_reduction_bam']):
        pysam.index(meta['after_reduction_bam'])

        # remove all reads that fall outside of region of interest
        # warning : this is the slow part of the script
        logging.debug('Step 2. reducing bam for speed for ' + meta['sorted_bam']) # pylint: disable=W1201
        without(meta['after_reduction_bam'], meta['removing_outside_matches'], meta['junk_bam'], meta['subregion_bed']) # pylint: disable=C0301

    if os.path.exists(meta['removing_outside_matches']):
        pysam.index(meta['removing_outside_matches'])

        # get only reads that are within subrange
        logging.debug('Step 3. final reduction for ' + meta['sorted_bam']) # pylint: disable=W1201
        within(meta['removing_outside_matches'], meta['final_bam'], subrange)

        if os.path.exists(meta['final_bam']):
            pysam.index(meta['final_bam'])

    logging.info('Amplicon bam file created for ' + meta['file_name'] + ' over ' + subrange) # pylint: disable=W1201

    return [meta['file_name'], meta['initial_bam'], name]
