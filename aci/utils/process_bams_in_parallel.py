import concurrent.futures
import logging

from .read_and_assign import read_and_assign


def process_bams_in_parallel(bam_files, bed_intervals, temp_dir):
    logging.info("Reading bams and assigning intervals")
    results = []

    with concurrent.futures.ProcessPoolExecutor() as executor:

        futures = [
            executor.submit(read_and_assign, bam, bed_intervals, temp_dir)
            for bam in bam_files
        ]
        for future in concurrent.futures.as_completed(futures):
            df = future.result()
            results.append(df)

    logging.info("All reads have been assigned to prospective intervals")
    return results
