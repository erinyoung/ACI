import pandas as pd
import pytest
from unittest import mock
from aci.utils.plotting_amplicons import plotting_amplicons

def test_plotting_amplicons(tmp_path):
    # Sample dataframes
    df = pd.DataFrame({
        "bam": ["sample1", "sample2"],
        "amp1": [10, 20],
        "amp2": [15, 25]
    })
    min_df = pd.DataFrame({
        "bam": ["sample1", "sample2"],
        "amp1": [5, 10],
        "amp2": [7, 12]
    })

    out_dir = tmp_path

    # Patch to_csv and plotting_boxplot
    with mock.patch.object(pd.DataFrame, "to_csv") as mock_to_csv, \
         mock.patch("aci.utils.plotting_amplicons.plotting_boxplot") as mock_plotting_boxplot:

        plotting_amplicons(df.copy(), min_df.copy(), str(out_dir))

        # Check to_csv called twice with expected filenames
        expected_calls = [
            mock.call(f"{out_dir}/amplicon_depth.csv", index=False),
            mock.call(f"{out_dir}/amplicon_min_depth.csv", index=False)
        ]
        mock_to_csv.assert_has_calls(expected_calls, any_order=False)

        # Check plotting_boxplot called twice
        assert mock_plotting_boxplot.call_count == 2

        # Check first call args (df plot)
        first_df_arg, first_d_arg = mock_plotting_boxplot.call_args_list[0][0]
        assert list(first_df_arg.columns) == ["amp1", "amp2"]
        assert first_d_arg["file"] == f"{out_dir}/amplicon_depth.png"

        # Check second call args (min_df plot)
        second_df_arg, second_d_arg = mock_plotting_boxplot.call_args_list[1][0]
        assert list(second_df_arg.columns) == ["amp1", "amp2"]
        assert second_d_arg["file"] == f"{out_dir}/amplicon_min_depth.png"
