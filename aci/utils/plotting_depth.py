#!/usr/bin/env python

"""Getting coverage ready for plotting"""

import logging

from .split_dataframe import split_dataframe
from .plotting_boxplot import plotting_boxplot


def plotting_depth(df, out):
    """Generate depth plots for each references (ref)"""

    df["ref"] = df["ref"].astype(str)
    df.to_csv(f"{out}/overall_depth.csv", index=False)
    references = df["ref"].unique()

    for ref in references:
        ref_df = df[df["ref"] == ref].copy()

        split_df = split_dataframe(ref_df)

        # Prepare for boxplot
        split_df["ungroup"] = split_df["group"] * 500
        split_df = split_df.drop(columns=["pos", "group"])
        split_df = split_df.set_index("ungroup")
        split_df = split_df.transpose()

        logging.debug(f"Restructured coverage for {ref}")
        logging.debug(split_df)

        # Plot
        plot_config = {
            "title": f"Coverage - {ref}",
            "ylabel": "Mean depth",
            "xlabel": "Genomic position",
            "file": f"{out}/{ref}_depth.png",
        }

        plotting_boxplot(split_df, plot_config)
