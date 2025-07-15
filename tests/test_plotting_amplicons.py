import pytest
import pandas as pd
from unittest import mock
from aci.utils.plotting_amplicons import plotting_amplicons


@mock.patch("aci.utils.plotting_amplicons.plotting_boxplot")
@mock.patch("matplotlib.pyplot.savefig")
@mock.patch("matplotlib.pyplot.close")
def test_plotting_amplicons(mock_close, mock_savefig, mock_plotting_boxplot, tmp_path):
    # Create minimal df and min_df including the 'bam' column
    df = pd.DataFrame(
        {
            "bam": ["sample1", "sample2"],
            "amp1": [10, 15],
            "amp2": [20, 25],
        }
    )

    min_df = pd.DataFrame(
        {
            "bam": ["sample1", "sample2"],
            "amp1": [5, 7],
            "amp2": [10, 12],
        }
    )

    out_dir = tmp_path

    plotting_amplicons(df, min_df, str(out_dir))

    # plotting_boxplot should be called at least twice for the summary plots
    assert mock_plotting_boxplot.call_count >= 2

    # savefig and close should be called for per sample plots
    assert mock_savefig.call_count == len(df)
    assert mock_close.call_count == len(df)
