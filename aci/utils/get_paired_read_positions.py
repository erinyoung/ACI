import os
import logging
import pysam
import pandas as pd


def get_paired_read_positions(bam_path, bed_trees):
    bam_name = os.path.basename(bam_path)
    assignments = []

    r1_rows = []
    r2_rows = []

    with pysam.AlignmentFile(bam_path, "rb") as bamfile:
        for read in bamfile.fetch(until_eof=True):
            if read.is_unmapped:
                continue

            row = {
                "read_name": read.query_name,
                "chrom": read.reference_name,
                "start": read.reference_start,
                "end": read.reference_end,
            }

            if read.is_read1:
                r1_rows.append(row)
            elif read.is_read2:
                r2_rows.append(row)

    # Convert to DataFrames
    r1_df = pd.DataFrame(r1_rows).rename(
        columns={"chrom": "chrom_R1", "start": "read_start_R1", "end": "read_end_R1"}
    )
    r2_df = pd.DataFrame(r2_rows).rename(
        columns={"chrom": "chrom_R2", "start": "read_start_R2", "end": "read_end_R2"}
    )

    # Merge paired reads
    merged_df = pd.merge(r1_df, r2_df, on="read_name")
    merged_df = merged_df[merged_df["chrom_R1"] == merged_df["chrom_R2"]]
    merged_df["chrom"] = merged_df["chrom_R1"]
    merged_df["start"] = merged_df[
        ["read_start_R1", "read_start_R2", "read_end_R1", "read_end_R2"]
    ].min(axis=1)
    merged_df["end"] = merged_df[
        ["read_start_R1", "read_start_R2", "read_end_R1", "read_end_R2"]
    ].max(axis=1)

    # Find overlapping intervals
    for _, row in merged_df.iterrows():

        if row["chrom"] in bed_trees:
            for interval in bed_trees[row["chrom"]][row["start"] : row["end"]]:
                assignments.append(
                    {
                        "read_name": row["read_name"],
                        "chrom": row["chrom"],
                        "read_start": row["start"],
                        "read_end": row["end"],
                        "amplicon": interval.data,
                        "bam": bam_name,
                    }
                )

    logging.debug(f"assignements: {assignments}")

    return pd.DataFrame(assignments)
