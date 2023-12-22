#!/usr/bin/env python

""" Takes a bam file and 
    1. checks to see if bam file is paired or single end reads
    2. then reduces bam file to those reads in specified subregion
    2a. if paired, restricts reads to those that are correctly paired
    2b. if single, restricts reads to those that are within region """

import os
import pysam

def within(bam0, bam1, subregion):
    """ reduces reads to those within subregion """


    if os.path.exists(bam0):
        single_check = int(pysam.view('-c', '-f',  '1', bam0))
        if single_check == 0 :
            pysam.view('-bh', '-o', bam1, bam0, subregion, catch_stdout=False)
        else :
            pysam.view('-bh','-f2', '-o', bam1, bam0, subregion, catch_stdout=False)
