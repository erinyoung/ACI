#!/usr/bin/env python

""" Gets coverage for bam over subrange """

import logging
import os
import pysam

def get_coverage(meta, region):
    """ Gets coverage for bam over subrange """

    ref   = region.split(':')[0]
    start = int(region.split(':')[1])
    end   = int(region.split(':')[2])
    reg   = ref + ':' + str(start) + '-' + str(end)

    name  = region.split(':')[3]
    bam   = meta['tmp'] + name + '.4.' + meta['file_name']

    if os.path.exists(bam):
        # get the coverage of the region (finally!)
        logging.debug('Getting coverage for ' + meta['file_name'] + ' over ' + reg) # pylint: disable=C0301
        logging.debug(pysam.coverage('--no-header', bam, '-r', reg).strip())
        cov = float(pysam.coverage('--no-header', bam, '-r', reg).split()[6])
    else:
        cov = float(0.0)

    logging.debug('The coverage for ' + meta['file_name'] + ' over ' + region + ' is ' + str(cov)) # pylint: disable=W1201,C0301

    return cov
