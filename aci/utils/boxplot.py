#!/usr/bin/env python

""" Graphs the dataframe """

import matplotlib.pyplot as plt

def without(df, out):
    """ graphs the dataframe """

    # writing results to a file
    df.to_csv(out + '/amplicon_depth.csv', index=False)

    # getting rid of column with all the bam names
    df.drop('bam', axis=1, inplace=True)

    boxplot = df.boxplot(fontsize=5, rot=90, figsize=(15,8), grid=False)
    boxplot.plot()
    plt.title('Primer Assessment')
    boxplot.set_ylabel('meandepth')
    boxplot.set_xlabel('amplicon name')
    boxplot.figure.savefig(out + '/amplicon_depth.png', bbox_inches='tight')
    plt.close()
