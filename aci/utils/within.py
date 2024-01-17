#!/usr/bin/env python

""" Takes a bam file and 
    1. checks to see if bam file is paired or single end reads
    2. then reduces bam file to those reads in specified subregion
    2a. if paired, restricts reads to those that are correctly paired
    2b. if single, restricts reads to those that are within region """

import logging
import os
import pysam

def within(initial_bam, final_bam, subregion):
    """ reduces reads to those within subregion """

    logging.debug(f"Initial bam is {initial_bam}") # pylint: disable=W1203
    logging.debug(f"Final bam is {final_bam}") # pylint: disable=W1203
    logging.debug(f"Region is {subregion}" ) # pylint: disable=W1203

    if os.path.exists(initial_bam):
        single_check = int(pysam.view('-c', '-f',  '1', initial_bam))
        if single_check == 0 :
            pysam.view('-bh', '-o', final_bam, initial_bam, subregion, catch_stdout=False)
        else :
            pysam.view('-bh','-f2', '-o', final_bam, initial_bam, subregion, catch_stdout=False)
