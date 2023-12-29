#!/usr/bin/env python

""" Graphs the dataframe """

import matplotlib.pyplot as plt

def plotting_boxplot(df, d):
    """ graphs the dataframe """

    boxplot = df.boxplot(fontsize=5, rot=90, figsize=(15,8), grid=False)
    boxplot.plot()
    plt.title(d['title'])
    boxplot.set_ylabel(d['ylabel'])
    boxplot.set_xlabel(d['xlabel'])
    boxplot.figure.savefig(d['file'], bbox_inches='tight')
    plt.close()
