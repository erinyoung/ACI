import logging
import os
import pysam


def is_paired_bam(bam_path, num_reads_to_check=1000):
    """checks to see if bam file is paired"""

    filename = os.path.basename(bam_path)
    logging.info(f"Checking if {filename} is paired")

    with pysam.AlignmentFile(bam_path, "rb") as bam:
        for i, read in enumerate(bam):
            if i >= num_reads_to_check:
                break
            if read.is_paired:
                logging.info(f"{filename} is paired")
                return True
    logging.info(f"{filename} is unpaired")

    return False
