import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial

from .read_and_assign import read_and_assign
from .divide_chrom_by_span import divide_chrom_by_span

def process_bams_in_parallel(bam_files, bed_intervals, args, temp_dir):
    logging.info("Reading bams and assigning intervals")
    results = []

    region_list = divide_chrom_by_span(bed_intervals, args.threads)

    tasks = []

    for bam in bam_files:
        for region in region_list:
            tasks.append((bam, region))

    # Use ProcessPoolExecutor to parallelize
    results = []
    # for bam in bam_files:
    #     for region in region_list:
    #         result = read_and_assign(bam, bed_intervals, region, args, temp_dir)
    #         if result:
    #             results.append(result)

    # Use ProcessPoolExecutor to parallelize
    with ProcessPoolExecutor(max_workers=args.threads) as executor:
        futures = [
            executor.submit(read_and_assign, bam, bed_intervals, region, args, temp_dir)
            for bam, region in tasks
        ]
        for future in as_completed(futures):
            results.append(future.result())

    logging.info("All reads have been assigned to prospective intervals")
    return results