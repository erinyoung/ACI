#!/usr/bin/env python3
import logging
import os
import sys
import tempfile
from importlib.metadata import version, PackageNotFoundError

import pandas as pd
import matplotlib
# Force backend to avoid display errors on headless servers
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

from concurrent.futures import ProcessPoolExecutor, as_completed

# --- Local Imports ---
from aci.utils.parse_args import parse_args
from aci.utils.io import prep
from aci.logic.bed_parser import parse_bed
from aci.logic.counter import count_amplicons_in_bam
from aci.logic.report import (
    generate_dropout_report, 
    generate_masking_beds, 
    generate_uniformity_report
)
from aci.plotting.plotting_amplicons import plotting_amplicons
from aci.plotting.heatmap import plot_heatmap
from aci.logic.genome_depth import genome_depth
from aci.plotting.plotting_depth import plotting_depth

def main():
    # 1. Get Dynamic Version
    try:
        pkg_version = version("amplicon_coverage_inspector")
    except PackageNotFoundError:
        pkg_version = "unknown"

    args = parse_args(pkg_version)

    logging.basicConfig(
        format="%(asctime)s - %(message)s",
        datefmt="%H:%M:%S",
        level=args.loglevel.upper(),
    )

    # 2. Validate Inputs
    if not os.path.exists(args.bed):
        logging.critical(f"BED file not found: {args.bed}")
        sys.exit(2)

    if not os.path.exists(args.out):
        os.makedirs(args.out)

    logging.info(f"ACI: v{pkg_version}")
    logging.info(f"Output: {args.out}")

    # --- PART 1: PARSE BED ---
    logging.info(f"Parsing BED file: {args.bed}")
    amplicons = parse_bed(args.bed)
    
    if not amplicons:
        logging.critical("No amplicons found in BED file! Check format.")
        sys.exit(1)

    # --- PART 2: PROCESS BAMS ---
    # Use a temporary directory for intermediate sorted BAMs
    # args.tmpdir defaults to None (System Tmp), or user defined path
    with tempfile.TemporaryDirectory(dir=args.tmpdir) as temp_dir:
        ready_bams = []
        logging.info("Preparing BAM files...")
        
        for bam in args.bam:
            # Create temp path for sorted file (if needed)
            temp_bam_path = os.path.join(temp_dir, os.path.basename(bam))
            final_bam = prep(bam, temp_bam_path, args.threads)
            ready_bams.append(final_bam)

        logging.info(f"Counting reads (Max/Min Logic) on {args.threads} threads...")
        results = []
        all_read_assignments = []
        
        with ProcessPoolExecutor(max_workers=args.threads) as executor:
            future_to_bam = {
                executor.submit(count_amplicons_in_bam, bam, amplicons): bam 
                for bam in ready_bams
            }
            
            for future in as_completed(future_to_bam):
                bam_name = os.path.basename(future_to_bam[future])
                try:
                    # Unpack the tuple returned by counter.py
                    count_data, read_data = future.result()
                    
                    results.extend(count_data)
                    all_read_assignments.extend(read_data)
                    
                    logging.info(f"Finished {bam_name}")
                except Exception as e:
                    logging.error(f"Failed processing {bam_name}: {e}")

        # --- PART 3: AGGREGATE, REPORT & PLOT ---
        if not results:
            logging.critical("No results generated! Check BED coordinates match BAM references.")
            sys.exit(1)

        logging.info("Aggregating results...")
        df = pd.DataFrame(results)
        
        # A. Save Debug Read Assignments
        reads_csv = os.path.join(args.out, "amplicon_read_assignments.csv")
        logging.info(f"Saving read assignments log to {reads_csv}")
        pd.DataFrame(all_read_assignments).to_csv(reads_csv, index=False)

        # B. Pivot DataFrames
        # Max = Lenient (Overlap)
        max_df = df.pivot_table(
            index='bam', 
            columns='amplicon', 
            values='max_count', 
            aggfunc='sum'
        ).fillna(0).reset_index()

        # Min = Strict (Unique)
        min_df = df.pivot_table(
            index='bam', 
            columns='amplicon', 
            values='min_count', 
            aggfunc='sum'
        ).fillna(0).reset_index()

        # C. Generate Reports
        logging.info("Generating QC reports...")
        
        # Convert percentage (e.g. 50) to decimal (0.5) for logic
        fail_decimal = args.fail_percentage / 100.0
        
        # 1. Dropout Report (TSV)
        generate_dropout_report(
            min_df, 
            args.out, 
            threshold=args.fail_threshold, 
            failure_cutoff=fail_decimal
        )
        
        # 2. Masking BEDs
        generate_masking_beds(
            min_df, 
            amplicons, 
            args.out, 
            threshold=args.fail_threshold
        )
        
        # 3. Uniformity & Efficiency (Returns DF for plotting)
        efficiency_df = generate_uniformity_report(max_df, args.out)

        # D. Generate Plots
        logging.info("Generating visualizations...")
        try:
            # Standard Boxplots & Line Graphs
            plotting_amplicons(max_df, min_df, args.out)
            
            # Log-Scale Heatmaps (Depth)
            plot_heatmap(
                max_df, 
                os.path.join(args.out, "heatmap_max_depth.png"), 
                "Max Depth Heatmap (Lenient/Overlap)",
                log_scale=True
            )
            plot_heatmap(
                min_df, 
                os.path.join(args.out, "heatmap_min_depth.png"), 
                "Min Depth Heatmap (Strict/Unique)",
                log_scale=True
            )
            
            # Linear-Scale Heatmap (Efficiency)
            if efficiency_df is not None:
                plot_heatmap(
                    efficiency_df,
                    os.path.join(args.out, "heatmap_efficiency.png"),
                    "Amplicon Efficiency (% of Total Reads)",
                    log_scale=False
                )

            logging.info("Plots saved successfully.")
        except Exception as e:
            logging.error(f"Plotting failed: {e}")

        # --- PART 4: LEGACY GENOME DEPTH ---
        logging.info("Calculating overall genome depth...")
        dfs = []
        for bam in ready_bams:
            dfs.append(genome_depth(bam))
        
        if dfs:
            df_pysam = pd.concat(dfs, ignore_index=True)
            plotting_depth(df_pysam, args.out)

    logging.info("ACI Complete.")

if __name__ == "__main__":
    main()