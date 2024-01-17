#!/usr/bin/env python
# pylint: disable=logging-fstring-interpolation

""" Takes a bed file and turns the lines into strings """

import logging
import sys

def get_regions(meta, bed):
    """ Takes a bed file and turns the lines into strings """

    regions = []
    names   = []
    with open(bed, encoding="utf-8") as file:
        for line in file:
            ref   = str(line.split('\t')[0])
            start = str(int(line.split('\t')[1]))
            end   = str(int(line.split('\t')[2]))
            name  = str(line.split('\t')[3])
            regions.append(ref + ':' + start + ':' + end + ':' + name)
            names.append(name)

            bed = meta['tmp'] + name + '.bed'
            if int(start) <= 1:
                with open(bed, mode='wt', encoding="utf-8") as file:
                    file.write(ref + '\t' + str(int(end) + 1) + '\t5000000\n')
            else:
                with open(bed, mode='wt', encoding="utf-8") as file:
                    line1 = ref + '\t' + str('0') + '\t' + str(int(start) - 1) + '\n'
                    line2 = ref + '\t' + str(int(end) + 1) + '\t5000000\n'
                    logging.debug(f"line 1 is {line1.strip()} in {bed}")
                    logging.debug(f"line 2 is {line2.strip()} in {bed}")
                    file.write(line1 + line2)

    logging.debug('Regions extracted from bedfile:')
    logging.debug(regions)

    # making sure region names are unique
    if len(names) != len(sorted(set(names))):
        logging.critical("Names in bedfiles are not unique! Exiting.")
        sys.exit(1)

    return regions
