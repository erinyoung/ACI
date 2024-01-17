#!/usr/bin/env python
# pylint: disable=logging-fstring-interpolation

""" Gets coverage for bam over subrange """

import logging
import os
import pysam

def get_coverage(bam, subrange):
    """ Gets coverage for bam over subrange """

    if os.path.exists(bam):
        # get the coverage of the region (finally!)
        logging.debug('Getting coverage for ' + bam + ' over ' + subrange)
        cov_line = pysam.coverage('--no-header', bam, '-r', subrange).strip()
        logging.debug(f"pysam coverage line : {cov_line}")
        cov = float(cov_line.split()[6])
    else:
        cov = 0.0

    logging.debug(f"The coverage for {bam} over {subrange} is {str(cov)}")

    return cov
