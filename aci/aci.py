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
import pandas as pd

from utils.amplicon_depth   import amplicon_depth   # pylint: disable=E0401
from utils.column_names     import column_names     # pylint: disable=E0401
from utils.get_regions      import get_regions      # pylint: disable=E0401
from utils.plotting_boxplot import plotting_boxplot # pylint: disable=E0401
from utils.prep             import prep             # pylint: disable=E0401
from utils.subregion        import subregion        # pylint: disable=E0401

# about 30 seconds per artic V3 primer on SRR13957125
# $ samtools coverage SRR13957125.sorted.bam
# #rname      startpos endpos numreads covbases coverage meandepth meanbaseq meanmapq
# MN908947.3  1        29903  1141595  29827    99.7458  5350.27   37.3      60
# 15000 - 16500

#logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%y-%b-%d %H:%M:%S', level=logging.INFO) # pylint: disable=C0301

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%y-%b-%d %H:%M:%S', level=logging.DEBUG) # pylint: disable=C0301

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bam', nargs = '+', required = True, type = str, help='(required) input bam file(s)')
parser.add_argument('-d', '--bed', required = True, type = str, help ='(required) amplicon bedfile')
parser.add_argument('-o', '--out', required = False, type = str, help='directory for results', default='aci')
parser.add_argument('-t', '--threads', required = False, type = int, help='specifies number of threads to use', default=4)
parser.add_argument('-v', '--version', help='print version and exit', action='version', version='%(prog)s 1.0.20231222')
args = parser.parse_args()

if __name__ == "__main__":

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

    ##### ----- ----- ----- ----- ----- #####
    ##### Part 1. Amplicon depths       #####
    ##### ----- ----- ----- ----- ----- #####

    bed       = args.bed
    out       = args.out
    threads   = args.threads

    # setting up the dataframe
    columns   = column_names(bed)
    df        = pd.DataFrame(columns= ['bam'] + columns)
    df['bam'] = args.bam
    logging.debug('Initial empty dataframe:')
    logging.debug(df)

    # getting regions for parallel processing
    regions = get_regions(bed)

    meta = {}
    for bam in args.bam:
        meta[bam]                       = {}
        meta[bam]['initial_bam']        = bam
        meta[bam]['out']                = out
        meta[bam]['file_name']          = os.path.basename(bam)
        meta[bam]['initial_sorted_bam'] = out + '/tmp.' + os.path.basename(bam)
        meta[bam]['initial_sorted_bai'] = meta[bam]['initial_sorted_bam'] + '.bai'

        logging.info('Sorting and indexing ' + meta[bam]['file_name']) # pylint: disable=W1201
        prep(meta[bam]['initial_bam'], meta[bam]['initial_sorted_bam'], threads)
    logging.info('Finished sorting and indexing')

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

    plotting_boxplot(df, out)

    logging.info('Depth for amplicons is saved in '  + args.out + '/amplicon_depth.csv') # pylint: disable=W1201
    logging.info('An boxplot of these depths is at ' + args.out + '/amplicon_depth.png') # pylint: disable=W1201

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


    logging.debug('Deleting tmp files')
    for bam in args.bam:
        if os.path.exists(meta[bam]['initial_sorted_bam']):
            os.remove(meta[bam]['initial_sorted_bam'])
        if os.path.exists(meta[bam]['initial_sorted_bai']):
            os.remove(meta[bam]['initial_sorted_bai'])

    logging.info('ACI is complete! (I hope all your primers are behaving as expected!)')
