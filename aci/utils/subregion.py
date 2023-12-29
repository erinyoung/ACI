#!/usr/bin/env python

""" Convert region string in script to something useable """

import logging

def subregion(region, bed):
    """ Creates string and bedfile """

    # create string
    ref   = region.split(':')[0]
    start = int(region.split(':')[1])
    end   = int(region.split(':')[2])
    reg   = ref + ':' + str(start) + '-' + str(end)

    # create bedfile
    if start <= 1:
        with open(bed, mode='wt', encoding="utf-8") as file:
            file.write(ref + '\t' + str(end + 1) + '\t5000000\n')
    else:
        with open(bed, mode='wt', encoding="utf-8") as file:
            line1 = ref + '\t' + str('0') + '\t' + str(start - 1) + '\n'
            line2 = ref + '\t' + str(end + 1) + '\t5000000\n'
            logging.debug('line 1 is ' + line1.strip() + ' in ' + bed)
            logging.debug('line 2 is ' + line2.strip() + ' in ' + bed)
            file.write(line1 + line2)

    logging.debug('The subrange is ' + reg) # pylint: disable=W1201

    return reg
