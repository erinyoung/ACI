import os
import logging
import pysam
import pandas as pd

# pylint: disable=duplicate-code

def get_paired_read_positions(bam_file_path, bed_trees):
    bam = pysam.AlignmentFile(bam_file_path, "rb")

    assignments = []

    # Iterate through BAM assuming it's sorted by read name
    prev_read = None

    for read in bam.fetch(until_eof=True):
        # Skip improper, secondary, or supplementary reads
        if not read.is_proper_pair or read.is_secondary or read.is_supplementary:
            continue

        if prev_read is None:
            prev_read = read
            continue

        # If current and previous reads are from the same pair
        if read.query_name == prev_read.query_name:
            # Assign properly based on read1/read2 flag
            if read.is_read1:
                read1, read2 = read, prev_read
            else:
                read1, read2 = prev_read, read

            chrom = read.reference_name
            start = min(read1.reference_start, read2.reference_start)
            end = max(read1.reference_end, read2.reference_end)

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
            # Reset for next pair
            prev_read = None

        else:
            # If names don't match, assume the previous read is unpaired
            prev_read = read

    bam.close()
    return pd.DataFrame(assignments)
