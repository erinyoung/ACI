#!/usr/bin/env python

"""Graphs the dataframe"""

import logging
import matplotlib.pyplot as plt

from .plotting_boxplot import plotting_boxplot


def plotting_amplicons(df, min_df, out):
    """graphs the dataframe"""

    # writing results to a file
    df.to_csv(f"{out}/amplicon_depth.csv", index=False)
    min_df.to_csv(f"{out}/amplicon_min_depth.csv", index=False)

    # getting rid of column with all the bam names
    max_df = df.drop("bam", axis=1).astype(float)
    min_df = min_df.drop("bam", axis=1).astype(float)

    min_df = min_df.astype(float)
    logging.debug(max_df.to_csv())
    logging.debug(min_df.to_csv())

    max_d = {
        "title": "Primer Assessment",
        "ylabel": "mean depth",
        "xlabel": "amplicon name",
        "file": f"{out}/amplicon_depth.png",
    }
    plotting_boxplot(max_df, max_d)

    min_d = {
        "title": "Primer Assessment",
        "ylabel": "mean depth",
        "xlabel": "amplicon name",
        "file": f"{out}/amplicon_min_depth.png",
    }
    plotting_boxplot(min_df, min_d)

    # Now plot per BAM/sample (per row)
    for i, bam_name in enumerate(df["bam"]):
        # Extract row data for this sample
        max_vals = max_df.iloc[i]
        min_vals = min_df.iloc[i]

        _, ax = plt.subplots(figsize=(10, 5))
        x = max_vals.index  # amplicon names
        x_pos = range(len(x))
        ax.plot(x_pos, max_vals, label="Max Depth", marker="o")
        ax.plot(x_pos, min_vals, label="Min Depth", marker="x")

        ax.set_xticks(x_pos)
        ax.set_xticklabels(x, rotation=90)

        ax.set_title(f"Primer Assessment - {bam_name}")
        ax.set_xlabel("Amplicon Name")
        ax.set_ylabel("Depth")
        ax.legend()
        plt.tight_layout()

        plot_file = f"{out}/amplicon_depth_{bam_name}.png"
        plt.savefig(plot_file)
        plt.close()

        logging.info(f"Saved per-sample plot: {plot_file}")
