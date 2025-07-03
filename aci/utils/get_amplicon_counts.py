import pandas as pd


def get_amplicon_counts(interval_files, amplicon_names):
    """getting the read counts for each amplicon"""

    # Create an empty DataFrame with columns for amplicon names
    max_amplicon_df = pd.DataFrame(columns=["bam"] + amplicon_names)
    max_amplicon_df.columns = max_amplicon_df.columns.astype(str)

    min_amplicon_df = pd.DataFrame(columns=["bam"] + amplicon_names)
    min_amplicon_df.columns = min_amplicon_df.columns.astype(str)

    for interval_file in interval_files:

        df = pd.read_csv(interval_file)
        df.columns = df.columns.astype(str)

        # getting maximum coverage
        max_count_df = df.groupby(["bam", "amplicon"]).size().unstack(fill_value=0)

        max_count_df = max_count_df.reset_index()
        max_count_df.columns = max_count_df.columns.astype(str)

        max_amplicon_df = pd.concat([max_amplicon_df, max_count_df], ignore_index=True)
        max_amplicon_df = max_amplicon_df.infer_objects(copy=False).fillna(0)

        # focus on reads that span only one interval
        df_unique = df[~df["read_name"].duplicated(keep=False)]

        min_count_df = (
            df_unique.groupby(["bam", "amplicon"]).size().unstack(fill_value=0)
        )
        min_count_df = min_count_df.reset_index()
        min_count_df.columns = min_count_df.columns.astype(str)
        min_amplicon_df = pd.concat([min_amplicon_df, min_count_df], ignore_index=True)
        min_amplicon_df = min_amplicon_df.infer_objects(copy=False).fillna(0)

    return max_amplicon_df, min_amplicon_df
