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
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pysam
# import subprocess
# import sys

from .utils import get_regions, prep

# about 30 seconds per artic V3 primer on SRR13957125
# $ samtools coverage SRR13957125.sorted.bam
# #rname      startpos endpos numreads covbases coverage meandepth meanbaseq meanmapq
# MN908947.3  1        29903  1141595  29827    99.7458  5350.27   37.3      60
# 15000 - 16500

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%y-%b-%d %H:%M:%S', level=logging.INFO) # pylint: disable=C0301

# logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%y-%b-%d %H:%M:%S', level=logging.DEBUG) # pylint: disable=C0301

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bam', nargs = '+', required = True, type = str, help='(required) input bam file(s)')
parser.add_argument('-d', '--bed', required = True, type = str, help ='(required) amplicon bedfile')
parser.add_argument('-o', '--out', required = False, type = str, help='directory for results', default='aci')
parser.add_argument('-t', '--threads', required = False, type = int, help='specifies number of threads to use', default=4)
parser.add_argument('-v', '--version', help='print version and exit', action='version', version='%(prog)s ' + '0.1.20230815')
args = parser.parse_args()

if __name__ == "__main__":

    version = '0.1.20230815'

    if not os.path.exists(args.bed):
        logging.critical('bedfile ' + args.bed + ' does not exist. Exiting')
        exit(1)

    if not os.path.exists(args.out):
        os.mkdir(args.out)

    logging.info('ACI version :\t\t'     + str(version))
    logging.info('Number of threads :\t' + str(args.threads))
    logging.info('Final directory :\t\t' + str(args.out))
    logging.info('Input bed file :\t\t'    + str(args.bed))
    logging.info('Input bam file(s) :\t' + ', '.join(args.bam))

    ##### ----- ----- ----- ----- ----- #####
    ##### Part 1. Amplicon depths       #####
    ##### ----- ----- ----- ----- ----- #####

    pool      = concurrent.futures.ThreadPoolExecutor(max_workers=args.threads)
    df        = pd.DataFrame([])
    df['bam'] = args.bam
    bed       = args.bed
    out       = args.out
    threads   = args.threads

    regions = get_regions(bed) 

# >>> d = {}
# >>> d['dict1'] = {}
# >>> d['dict1']['innerkey'] = 'value'
# >>> d['dict1']['innerkey2'] = 'value2'
# >>> d
# {'dict1': {'innerkey': 'value', 'innerkey2': 'value2'}}

    meta = {}
    for bam in args.bam:
        meta['bam']                = {}
        meta['initial_bam']        = bam
        meta['bam']['file_name']   = os.path.basename(bam)
        meta['initial_sorted_bam'] = out + '/tmp.' + os.path.basename(bam)

        logging.info('Sorting and indexing ' + meta['bam']['file_name'])
        prep(meta['bam'], threads)

    logging.info('Finished sorting and indexing')

    # logging.info('Getting depth for amplicons')
    # for input in list(itertools.product(args.bam, regions)):
    #     #pool.submit(amplicon_depth, df, input[0], input[1], False)
    #     amplicon_depth(df,input[0],input[1],False)
    #     logging.debug('Region: ' + input[1])
    # logging.debug('Finished getting depth for amplicons')

    # pool.shutdown(wait=True)

    # logging.debug('Deleting tmp files')
    # for bam in args.bam:
    #     bam0 = args.out + '/tmp.' + os.path.basename(bam) 
    #     os.remove(bam0)
    #     os.remove(bam0 + '.bai')

    logging.info('Depth for amplicons is saved in '  + args.out + '/amplicon_depth.csv')
    logging.info('An boxplot of these depths is at ' + args.out + '/amplicon_depth.png')

    # ##### ----- ----- ----- ----- ----- #####
    # ##### Part 2. Genome/bam depths     #####
    # ##### ----- ----- ----- ----- ----- #####
    # def genome_depth(df1, bam):
    #     file_name = os.path.basename(bam)
    #     df2 = pd.DataFrame([x.split('\t') for x in pysam.depth(bam).split('\n')])
    #     df2.columns = ['ref', 'pos', 'cov']
    #     df3 = pd.DataFrame(columns = ['bam'] + df2['pos'].to_list())
    #     df3.loc[1] = [bam] + df2['cov'].to_list()
    #     df1 = pd.merge(df1, df3, how = 'outer')

    # # now getting depth information for comparison
    # df1        = pd.DataFrame([])
    # df1['bam'] = args.bam

    # for bam in args.bam:
    #     genome_depth(df1, bam)

    # # dividing positions into group for boxplot
    # df1['group'] = (df1['pos'] / 500).apply(np.floor)
    # df1 = df1.drop(['ref', 'pos'], axis=1)

    # # getting a df for graphing
    # df2 = df1.groupby(['group']).mean().reset_index()
    # df2['start'] = (df2['group'] * 500).astype(int)
    # df2['end']   = (df2['group'] * 500 + 499).astype(int)
    # df2['pos']   = df2['start'].astype('str') + '-' + df2['end'].astype('str')

    # # remove depth file
    # os.remove(args.out + '/depth.txt')

    # # writing results to a file
    # df2.to_csv(args.out + '/genome_depth.csv', index=False)

    # groups=df2['pos'].to_list()

    # # getting rid of column with all the group names
    # df2 = df2.drop(['group', 'pos', 'start','end'], axis=1)

    # # switching columns (bam files) for rows (positions)
    # df2 = df2.transpose()
    # df2.columns=groups

    # # creating the boxplot
    # boxplot2 = df2.boxplot(fontsize=5, rot=90, figsize=(15,8), grid=False)
    # boxplot2.plot()
    # plt.title('Average depth across genome')
    # boxplot2.set_ylabel('meandepth')
    # boxplot2.set_xlabel('position (start-end)')
    # boxplot2.figure.savefig(args.out + '/genome_depth.png', bbox_inches='tight')
    # plt.close()

    # loggin.info('Depth for the genome from the bam file is saved in ' + args.out + '/genome_depth.csv')
    # loggin.info('An boxplot of these depths is at ' + args.out + '/genome_depth.png')

    logging.info('ACI is complete! (I hope all your primers are behaving as expected!)')
