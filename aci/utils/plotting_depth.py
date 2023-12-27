#!/usr/bin/env python

""" Graphs the dataframe """

import logging
import matplotlib.pyplot as plt

from .split_dataframe import split_dataframe
from .group_create import group_create
from .group_mean import group_mean

def plotting_depth(df, out):
    """ graphs the dataframe """

    df = split_dataframe(df)

    # writing results to a file
    df.to_csv(out + '/overall_depth.csv', index=False)

    df = df.drop('pos', axis=1)

    boxplot = df.boxplot(fontsize=5, rot=90, figsize=(15,8), grid=False)
    boxplot.plot()
    plt.title('Overall coverage')
    boxplot.set_ylabel('meandepth')
    boxplot.set_xlabel('region')
    boxplot.figure.savefig(out + '/overall_depth.png', bbox_inches='tight')
    plt.close()
