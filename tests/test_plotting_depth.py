import pandas as pd
import pandas.testing as pdt
from unittest import mock

from aci.plotting.plotting_depth import plotting_depth

# CHANGED: aci.utils.plotting_depth -> aci.plotting.plotting_depth
# Note: plotting_depth.py imports split_dataframe, so we patch where it is used
@mock.patch("aci.plotting.plotting_depth.split_dataframe")
@mock.patch("aci.plotting.plotting_depth.plotting_boxplot")
def test_plotting_depth(mock_plotting_boxplot, mock_split_dataframe, tmp_path):
    df = pd.DataFrame(
        {
            "bam": ["sample1", "sample2"],
            "pos": [1, 2],
            "group": [1, 2],
            "cov": [10, 20],
            "ref": ["chr1", "chr1"],
        }
    )

    df_after_split = pd.DataFrame(
        {
            "pos": [1, 2],
            "group": [1, 2],
            "cov": [10, 20],
            "ref": ["chr1", "chr1"],
        }
    )
    mock_split_dataframe.return_value = df_after_split

    out_dir = tmp_path

    plotting_depth(df, str(out_dir))

    # Check split_dataframe called exactly once
    assert mock_split_dataframe.call_count == 1

    # Check argument equality with pandas testing
    called_df = mock_split_dataframe.call_args[0][0]
    pdt.assert_frame_equal(called_df.reset_index(drop=True), df.reset_index(drop=True))