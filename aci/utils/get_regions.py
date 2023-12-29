#!/usr/bin/env python

""" Takes a bed file and turns the lines into strings """

import logging

def get_regions(bed):
    """ Takes a bed file and turns the lines into strings """

    regions = []
    with open(bed, encoding="utf-8") as file:
        for line in file:
            ref   = str(line.split('\t')[0])
            start = str(int(line.split('\t')[1]))
            end   = str(int(line.split('\t')[2]))
            name  = str(line.split('\t')[3])
            regions.append(ref + ':' + start + ':' + end + ':' + name)

    logging.debug('Regions extracted from bedfile:')
    logging.debug(regions)

    return regions
