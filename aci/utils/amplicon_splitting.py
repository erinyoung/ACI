#!/usr/bin/env python
# pylint: disable=logging-fstring-interpolation

"""Split processes by region in bedfile for concurrent"""

from .load_bed_intervals import load_bed_intervals
from .process_bams_in_parallel import process_bams_in_parallel
from .get_amplicon_counts import get_amplicon_counts


def amplicon_splitting(meta, args):
    """Split processes by region in bedfile for concurrent"""

    bed_trees, amplicon_names = load_bed_intervals(args.bed)
    print(bed_trees)
    print(amplicon_names)

    interval_files = process_bams_in_parallel(args.bam, bed_trees, meta["tmp"])
    max_df, min_df = get_amplicon_counts(interval_files, amplicon_names)

    return max_df, min_df
