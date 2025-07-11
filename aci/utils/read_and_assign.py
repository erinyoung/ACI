import logging
import os

from .is_paired import is_paired_bam
from .get_paired_read_positions import get_paired_read_positions
from .get_unpaired_read_positions import get_unpaired_read_positions

def read_and_assign(bam_path, bed_trees, region, args, temp_dir):
    """Identify which interval each read  or read pair is in"""
    filename = os.path.basename(bam_path)

    logging.info(f"Looking at reads in {region} in {filename}")
    paired = is_paired_bam(bam_path)
    assigned_file = f"{temp_dir}/assigned_reads_{region}_{filename}.csv"

    if paired:
        logging.debug(f"{filename} is paired")
        df = get_paired_read_positions(bam_path, bed_trees, region)
    else:
        logging.debug(f"{filename} is unpaired")
        df = get_unpaired_read_positions(bam_path, bed_trees)

    logging.info(f"Intervals assigned to {filename}")

    if df.empty:
        return False

    # writing to file so that everything is not stuck in memory
    df.columns = ["read_name", "chrom", "read_start", "read_end", "amplicon", "bam"]
    df.to_csv(assigned_file, index=False)

    return assigned_file
