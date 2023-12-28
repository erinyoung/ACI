#!/usr/bin/env python3

'''
Author: Erin Young

Description:

This script will find the coverage for each amplicon in a bedfile and then graph it.

EXAMPLE:
aci -b input.bam -d amplicon.bed -o out
'''

# https://packaging.python.org/en/latest/tutorials/packaging-projects/

# I tried to keep dependencies down...
import argparse
import concurrent.futures
import itertools
import logging
import os
import sys
import tempfile
import pandas as pd

from utils.amplicon_depth       import amplicon_depth       # pylint: disable=E0401
from utils.column_names         import column_names         # pylint: disable=E0401
from utils.get_regions          import get_regions          # pylint: disable=E0401
from utils.genome_depth         import genome_depth         # pylint: disable=E0401
from utils.plotting_amplicons   import plotting_amplicons   # pylint: disable=E0401
from utils.plotting_depth       import plotting_depth       # pylint: disable=E0401
from utils.prep                 import prep                 # pylint: disable=E0401
from utils.subregion            import subregion            # pylint: disable=E0401

# about 30 seconds per artic V3 primer on SRR13957125
# $ samtools coverage SRR13957125.sorted.bam
# #rname      startpos endpos numreads covbases coverage meandepth meanbaseq meanmapq
# MN908947.3  1        29903  1141595  29827    99.7458  5350.27   37.3      60
# 15000 - 16500

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bam', nargs = '+', required = True, type = str, help = '(required) input bam file(s)') # pylint: disable=C0301
parser.add_argument('-d', '--bed', required = True, type = str, help ='(required) amplicon bedfile')
parser.add_argument('-o', '--out', required = False, type = str, help = 'directory for results', default = 'aci') # pylint: disable=C0301
parser.add_argument('-log', '--loglevel', required = False, type = str, help = 'logging level', default = 'INFO') # pylint: disable=C0301
parser.add_argument('-t', '--threads', required = False, type = int, help = 'specifies number of threads to use', default=4) # pylint: disable=C0301
parser.add_argument('-v', '--version', help='print version and exit', action = 'version', version = '%(prog)s 1.0.20231222') # pylint: disable=C0301
args = parser.parse_args()

if __name__ == "__main__":

    ##### ----- ----- ----- ----- ----- #####
    ##### Part 0. Setup                 #####
    ##### ----- ----- ----- ----- ----- #####

    logging.basicConfig(format='%(asctime)s - %(message)s',
        datefmt = '%y-%b-%d %H:%M:%S',
        level=args.loglevel.upper())

    VERSION = '1.0.20231222'

    if not os.path.exists(args.bed):
        logging.critical('bedfile ' + args.bed + ' does not exist. Exiting') # pylint: disable=W1201
        sys.exit(2)

    if not os.path.exists(args.out):
        os.mkdir(args.out)

    logging.info('ACI version :\t\t'     + str(VERSION))        # pylint: disable=W1201
    logging.info('Number of threads :\t' + str(args.threads))   # pylint: disable=W1201
    logging.info('Final directory :\t\t' + str(args.out))       # pylint: disable=W1201
    logging.info('Input bed file :\t\t'  + str(args.bed))       # pylint: disable=W1201
    logging.info('Input bam file(s) :\t' + ', '.join(args.bam)) # pylint: disable=W1201

    bed       = args.bed
    out       = args.out
    threads   = args.threads
    temp_dir  = tempfile.TemporaryDirectory(dir = args.out) # pylint: disable=R1732

    meta = {}
    filenames = []
    for bam in args.bam:
        meta[bam]                       = {}
        meta[bam]['initial_bam']        = bam
        meta[bam]['out']                = out
        meta[bam]['tmp']                = temp_dir.name + '/'
        meta[bam]['file_name']          = os.path.basename(bam)
        meta[bam]['sorted_bam'] = meta[bam]['tmp'] + os.path.basename(bam)
        meta[bam]['sorted_bai'] = meta[bam]['sorted_bam'] + '.bai'
        filenames.append(meta[bam]['file_name'])

        logging.info('Sorting and indexing ' + meta[bam]['file_name']) # pylint: disable=W1201
        prep(meta[bam]['initial_bam'], meta[bam]['sorted_bam'], threads)
    logging.info('Finished sorting and indexing')

    logging.debug('the filenames for all the bam files are')
    logging.debug(filenames)

    ##### ----- ----- ----- ----- ----- #####
    ##### Part 1. Amplicon depths       #####
    ##### ----- ----- ----- ----- ----- #####

    # setting up the dataframe
    columns   = column_names(bed)
    df        = pd.DataFrame(columns= ['bam'] + columns)
    df['bam'] = filenames
    logging.debug('Initial empty dataframe:')
    logging.debug(df)

    # getting regions for parallel processing
    regions = get_regions(bed)

    logging.info('Getting depth for amplicons')
    logging.debug('List for parallel processing:')
    logging.debug(list(itertools.product(args.bam, regions)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        for bam, subregion in list(itertools.product(args.bam, regions)):
            results = [executor.submit(amplicon_depth, df, meta[bam], subregion)]
            # keeping the line below for testing
            # results = amplicon_depth(df, meta[bam], subregion)

        for f in concurrent.futures.as_completed(results):
            logging.debug(f.result())

    logging.debug('The final dataframe is:')
    logging.debug(df)

    plotting_amplicons(df, out)

    logging.info('Depth for amplicons is saved in '  + args.out + '/amplicon_depth.csv') # pylint: disable=W1201
    logging.info('An boxplot of these depths is at ' + args.out + '/amplicon_depth.png') # pylint: disable=W1201

    # ##### ----- ----- ----- ----- ----- #####
    # ##### Part 2. Genome/bam depths     #####
    # ##### ----- ----- ----- ----- ----- #####

    df_pysam = pd.DataFrame([])

    # TODO : Fix this so that it's concurrent friendly

    for bam in args.bam:
        df_pysam_results = genome_depth(meta[bam])
        df_pysam = pd.concat([df_pysam, df_pysam_results], ignore_index=True)

    logging.debug('The final pysam dataframe is:')
    logging.debug(df_pysam)

    plotting_depth(df_pysam, out)

    logging.info('Depth for the genome from the bam file is saved in ' + out + '/genome_depth.csv') # pylint: disable=W1201
    logging.info('An boxplot of these depths is at ' + out + '/genome_depth.png') # pylint: disable=W1201

    logging.info('ACI is complete! (I hope all your primers are behaving as expected!)')
