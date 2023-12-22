#!/usr/bin/env python

""" Use pysam to get depth for amplicon region """

import logging
import os
import pysam
from .subregion import subregion
from .within import within
from .without import without

def amplicon_depth(df, meta, region):
    """ Use pysam to get depth for amplicon region """

    name = region.split(':')[3]

    # pylint was complaining about the number of variables
    # so they're all dict values instead
    meta['after_reduction_bam']      = meta['out'] + '/tmp.' + name + '.1.' + meta['file_name']
    meta['removing_outside_matches'] = meta['out'] + '/tmp.' + name + '.2.' + meta['file_name']
    meta['junk_bam']                 = meta['out'] + '/tmp.' + name + '.3.' + meta['file_name']
    meta['final_bam']                = meta['out'] + '/tmp.' + name + '.4.' + meta['file_name']
    meta['subregion_bed']            = meta['out'] + '/tmp.' + name + '.'   + meta['file_name'] + '.bed' # pylint: disable=C0301
    logging.debug('The filenames are going to be :')
    logging.debug(meta)

    # getting subregion information and creating bedfile
    subrange  = subregion(region, meta['subregion_bed'])

    # reduce bam file to something smaller
    if os.path.exists(meta['initial_sorted_bam']):
        logging.debug('Step 1. reducing bam for speed for ' + meta['initial_sorted_bam']) # pylint: disable=W1201
        within(meta['initial_sorted_bam'], meta['after_reduction_bam'], subrange)

    if os.path.exists(meta['after_reduction_bam']):
        pysam.index(meta['after_reduction_bam'])

        # remove all reads that fall outside of region of interest
        # warning : this is the slow part of the script
        logging.debug('Step 2. reducing bam for speed for ' + meta['initial_sorted_bam']) # pylint: disable=W1201
        without(meta['after_reduction_bam'], meta['removing_outside_matches'], meta['junk_bam'], meta['subregion_bed']) # pylint: disable=C0301

    if os.path.exists(meta['removing_outside_matches']):
        pysam.index(meta['removing_outside_matches'])

        # get only reads that are within subrange
        logging.debug('Step 3. final reduction for ' + meta['initial_sorted_bam']) # pylint: disable=W1201
        within(meta['removing_outside_matches'], meta['final_bam'], subrange)

    if os.path.exists(meta['final_bam']):
        pysam.index(meta['final_bam'])

        # get the coverage of the region (finally!)
        logging.debug('Step 4. getting coverage for ' + meta['initial_sorted_bam'] + ' over ' + subrange) # pylint: disable=C0301
        logging.debug(pysam.coverage('--no-header', meta['final_bam'], '-r', subrange).strip())
        cov = float(pysam.coverage('--no-header', meta['final_bam'], '-r', subrange).split()[6])
    else:
        cov = float(0.0)
    logging.debug('The coverage for ' + meta['initial_sorted_bam'] + ' over ' + subrange + ' is ' + str(cov)) # pylint: disable=W1201,C0301

    # removing files
    tmpfiles = ['after_reduction_bam', 'removing_outside_matches', 'junk_bam', 'final_bam', 'subregion_bed'] # pylint: disable=C0301
    for file in tmpfiles:
        if os.path.exists(meta[file]):
            os.remove(meta[file])
        if os.path.exists(meta[file] + '.bai'):
            os.remove(meta[file] + '.bai')

    bamindex = df.index[df['bam'] == meta['initial_bam']]
    df.loc[bamindex, [region.split(':')[3]]] = cov

    return [meta['initial_bam'], name, cov]
