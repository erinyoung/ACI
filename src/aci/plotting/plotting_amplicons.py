#!/usr/bin/env python

"""Graphs the dataframe"""

import logging
import matplotlib.pyplot as plt
import os
import pandas as pd

# Import local helper (ensure plotting_boxplot is in the same folder)
from .plotting_boxplot import plotting_boxplot

def plotting_amplicons(max_df, min_df, out):
    """
    Graphs the Max (Lenient) and Min (Strict) dataframes.
    
    Args:
        max_df (pd.DataFrame): Rows=Samples, Cols=Amplicons (Cells = Overlap Counts)
        min_df (pd.DataFrame): Rows=Samples, Cols=Amplicons (Cells = Strict Counts)
        out (str): Output directory
    """

    # 1. Save Raw Data
    max_df.to_csv(os.path.join(out, "amplicon_max_depth.csv"), index=False)
    min_df.to_csv(os.path.join(out, "amplicon_min_depth.csv"), index=False)

    # 2. Prepare Data for Boxplots
    # Drop 'bam' column so we have a matrix of only numbers
    try:
        plot_max_df = max_df.drop("bam", axis=1).astype(float)
        plot_min_df = min_df.drop("bam", axis=1).astype(float)
    except KeyError:
        # Fallback if 'bam' is currently the index
        plot_max_df = max_df.astype(float)
        plot_min_df = min_df.astype(float)

    # 3. Plot MAX DEPTH (Lenient / Overlapping)
    max_config = {
        "title": "Max Amplicon Depth (Lenient/Overlap)",
        "ylabel": "Read Count",
        "xlabel": "Amplicon",
        "file": os.path.join(out, "amplicon_max_depth_boxplot.png"),
    }
    plotting_boxplot(plot_max_df, max_config)

    # 4. Plot MIN DEPTH (Strict / Unique)
    min_config = {
        "title": "Min Amplicon Depth (Strict/Unique)",
        "ylabel": "Read Count",
        "xlabel": "Amplicon",
        "file": os.path.join(out, "amplicon_min_depth_boxplot.png"),
    }
    plotting_boxplot(plot_min_df, min_config)

    # 5. Plot Per-Sample Comparison (Line Graph)
    # This visualizes the gap between Max and Min for each sample
    
    # Ensure 'bam' is available for iteration
    if "bam" in max_df.columns:
        sample_names = max_df["bam"]
        # Access data by integer location since we stripped the column
        max_matrix = plot_max_df
        min_matrix = plot_min_df
    else:
        sample_names = max_df.index
        max_matrix = max_df
        min_matrix = min_df

    for i, bam_name in enumerate(sample_names):
        # Extract row data
        max_vals = max_matrix.iloc[i]
        min_vals = min_matrix.iloc[i]

        plt.figure(figsize=(12, 6))
        
        x_labels = max_vals.index  # Amplicon names
        x_pos = range(len(x_labels))
        
        # Plot Max line
        plt.plot(x_pos, max_vals, label="Max Depth (Overlap)", 
                 color='skyblue', marker="o", linestyle='-', alpha=0.8)
        
        # Plot Min line
        plt.plot(x_pos, min_vals, label="Min Depth (Strict)", 
                 color='navy', marker="x", linestyle='--', alpha=0.8)

        # Fill the gap to highlight the "uncertainty" or "overlap" region
        plt.fill_between(x_pos, min_vals, max_vals, color='gray', alpha=0.1)

        plt.xticks(x_pos, x_labels, rotation=90, fontsize=8)
        plt.title(f"Amplicon Coverage: {bam_name}")
        plt.xlabel("Amplicon")
        plt.ylabel("Read Depth")
        plt.legend()
        plt.tight_layout()

        plot_file = os.path.join(out, f"depth_comparison_{bam_name}.png")
        plt.savefig(plot_file)
        plt.close()

        logging.info(f"Saved comparison plot: {plot_file}")