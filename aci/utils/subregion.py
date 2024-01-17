#!/usr/bin/env python

""" Convert region string in script to something useable """

import logging

def subregion(region):
    """ Creates string and bedfile """

    # create string
    ref   = region.split(':')[0]
    start = region.split(':')[1]
    end   = region.split(':')[2]
    reg   = ref + ':' + str(start) + '-' + str(end)

    name = region.split(':')[3]

    logging.debug(f"The region is {region}") # pylint: disable=W1203
    logging.debug(f"The subrange is {reg}") # pylint: disable=W1203
    logging.debug(f"The amplicon name is {name}") # pylint: disable=W1203

    return reg, name
