#!/usr/bin/env python
# pylint: disable=logging-fstring-interpolation

""" Split processes by region in bedfile for concurrent """

import logging
import concurrent.futures
import pandas as pd

from .amplicon_depth import amplicon_depth
from .get_regions import get_regions
from .column_names import column_names

def amplicon_splitting(meta, args):
    """ Split processes by region in bedfile for concurrent """

    # getting region for parallel processing
    regions = get_regions(meta, args.bed)
    #regions = ['MN908947.3:54:385:1', 'MN908947.3:342:704:2', 'MN908947.3:664:1004:3', 'MN908947.3:965:1312:4', 'MN908947.3:1264:1623:5', 'MN908947.3:1595:1942:6' ]

    logging.info('Getting depth for amplicons')
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        tasks = []
        for bam in args.bam:
            for subregion in regions:
                future = executor.submit(amplicon_depth, meta[bam], subregion)
                tasks.append(future)

        completed_tasks, _ = concurrent.futures.wait(tasks,return_when=concurrent.futures.ALL_COMPLETED) # pylint: disable=C0301
        results = [task.result() for task in completed_tasks]

    # setting up the dataframe
    columns   = column_names(args.bed)
    df        = pd.DataFrame(columns= ['bam'] + columns)
    df['bam'] = meta['filenames']
    logging.debug('Initial empty dataframe:')
    logging.debug(df)

    # NOTE : Had to be done outside of concurrent
    for bam, name, cov in results :
        bamindex = df.index[df['bam'] == bam]
        df.loc[bamindex, name] = cov

    df = df.fillna(0)

    return df
