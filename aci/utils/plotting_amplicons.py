#!/usr/bin/env python

""" Graphs the dataframe """

import logging
import matplotlib.pyplot as plt

def plotting_amplicons(df, out):
    """ graphs the dataframe """

    # writing results to a file
    df.to_csv(out + '/amplicon_depth.csv', index=False)

    # getting rid of column with all the bam names
    df = df.drop('bam', axis=1)

    df=df.astype(float)

    logging.debug(df)

    boxplot = df.boxplot(fontsize=5, rot=90, figsize=(15,8), grid=False)
    boxplot.plot()
    plt.title('Primer Assessment')
    boxplot.set_ylabel('meandepth')
    boxplot.set_xlabel('amplicon name')
    boxplot.figure.savefig(out + '/amplicon_depth.png', bbox_inches='tight')
    plt.close()
