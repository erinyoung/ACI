import os
import logging
import pysam
import pandas as pd

# pylint: disable=duplicate-code


def get_unpaired_read_positions(bam_file_path, bed_trees):
    bam = pysam.AlignmentFile(bam_file_path, "rb")

    assignments = []

    for read in bam.fetch(until_eof=True):
        # Skip secondary/supplementary/unmapped reads
        if read.is_secondary or read.is_supplementary or read.is_unmapped:
            continue

        chrom = read.reference_name
        start = read.reference_start
        end = read.reference_end

        if chrom in bed_trees:
            overlapping = bed_trees[chrom].overlap(start, end)
            for interval in overlapping:
                read_info = {
                    "read_name": read.query_name,
                    "chrom": chrom,
                    "read_start": start,
                    "read_end": end,
                    "amplicon": interval.data,
                    "bam": os.path.basename(bam_file_path),
                }
                assignments.append(read_info)

                logging.debug(f"reads : {read_info}")

    bam.close()
    logging.debug(f"assignements: {assignments}")

    return pd.DataFrame(assignments)
