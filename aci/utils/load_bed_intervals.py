import logging
import sys

from intervaltree import IntervalTree

def load_bed_intervals(bed_path):
    """getting intervals from bedfile"""

    logging.info("Getting intervals in bedfile")
    trees = {}
    names = []

    with open(bed_path, "r", encoding="utf-8") as f:
        for line in f:
            if len(line.strip().split()) < 4:
                logging.critical(
                    f"bedfile is missing columns. There are only {len(line.strip().split())}!"
                )
                sys.exit(1)
            chrom, start, end, name = line.strip().split()[:4]
            start, end = int(start), int(end)
            if chrom not in trees:
                trees[chrom] = IntervalTree()
            trees[chrom].addi(start, end, name)
            if name in names:
                logging.critical(
                    f"{bed_path} does not have unique names for amplicons!\nsee line {line}\n{name} has already been used!"
                )
                sys.exit(1)
            else:
                names.append(name)
    return trees, names
