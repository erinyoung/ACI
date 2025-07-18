#!/usr/bin/env python3
# pylint: disable=logging-fstring-interpolation

"""
Author: Erin Young

Description:

This script will find the coverage for each amplicon in a bedfile and then graph it.

EXAMPLE:
aci -b input.bam -d amplicon.bed -o out
"""

# I tried to keep dependencies down...
import logging
import os
import sys
import tempfile
import pandas as pd

from aci.utils.amplicon_splitting import amplicon_splitting
from aci.utils.genome_depth import genome_depth
from aci.utils.plotting_amplicons import plotting_amplicons
from aci.utils.plotting_depth import plotting_depth
from aci.utils.prep import prep
from aci.utils.parse_args import parse_args

# about 30 seconds per artic V3 primer on SRR13957125
# $ samtools coverage SRR13957125.sorted.bam
# #rname      startpos endpos numreads covbases coverage meandepth meanbaseq meanmapq
# MN908947.3  1        29903  1141595  29827    99.7458  5350.27   37.3      60
# 15000 - 16500


def main():
    """Use pysam to get depth for amplicon region and general coverage"""

    ##### ----- ----- ----- ----- ----- #####
    ##### Part 0. Setup                 #####
    ##### ----- ----- ----- ----- ----- #####

    version = "1.15.250702"

    args = parse_args(version)

    logging.basicConfig(
        format="%(asctime)s - %(message)s",
        datefmt="%y-%b-%d %H:%M:%S",
        level=args.loglevel.upper(),
    )

    if not os.path.exists(args.bed):
        logging.critical(f"bedfile {args.bed} does not exist. Exiting")
        sys.exit(2)

    if not os.path.exists(args.out):
        os.mkdir(args.out)

    logging.info(f"ACI version :\t\t{str(version)}")
    logging.info(f"Number of threads :\t{str(args.threads)}")
    logging.info(f"Final directory :\t\t{str(args.out)}")
    logging.info(f"Input bed file :\t\t{str(args.bed)}")
    logging.info(f"Input bam file(s) :\t{', '.join(args.bam)}")

    with tempfile.TemporaryDirectory(dir=args.out) as temp_dir:

        ##### ----- ----- ----- ----- ----- #####
        ##### Part 0. Sorting the bam file  #####
        ##### ----- ----- ----- ----- ----- #####

        sorted_bams = []
        for bam in args.bam:
            logging.info(f"Sorting and indexing {os.path.basename(bam)}")
            sorted_bam = prep(
                bam, 
                f"{temp_dir}/{os.path.basename(bam)}", 
                args.threads
            )
            sorted_bams.append(sorted_bam)
        logging.info(f"Finished sorting and indexing {os.path.basename(bam)}")

        ##### ----- ----- ----- ----- ----- #####
        ##### Part 1. Amplicon depths       #####
        ##### ----- ----- ----- ----- ----- #####

        max_df, min_df = amplicon_splitting(sorted_bams, args, temp_dir)

        plotting_amplicons(max_df, min_df, args.out)

        logging.info(f"Amplicon depth is saved in {args.out}/amplicon_depth.csv")
        logging.info(f"A boxplot of these depths is at {args.out}/amplicon_depth.png")

        # ##### ----- ----- ----- ----- ----- #####
        # ##### Part 2. Genome/bam depths     #####
        # ##### ----- ----- ----- ----- ----- #####

        df_pysam = pd.DataFrame([])

        # NOTE : Attempted with concurrent and this was just as fast

        for bam in sorted_bams:
            df_pysam_results = genome_depth(bam)
            df_pysam = pd.concat([df_pysam, df_pysam_results], ignore_index=True)

        plotting_depth(df_pysam, args.out)

        logging.info(f"Genome depth is saved in {args.out}/genome_depth.csv")
        logging.info(f"An boxplot of these depths is at {args.out}/genome_depth.png")

        # ##### ----- ----- ----- ----- ----- #####
        # ##### Fin                           #####
        # ##### ----- ----- ----- ----- ----- #####

        logging.info(
            "ACI is complete! (I hope all your primers are behaving as expected!)"
        )


if __name__ == "__main__":
    main()
