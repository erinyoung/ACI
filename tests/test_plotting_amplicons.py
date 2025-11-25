import pytest
import pandas as pd
from unittest import mock
from aci.plotting.plotting_amplicons import plotting_amplicons

# CHANGED: aci.utils -> aci.plotting
@mock.patch("aci.plotting.plotting_amplicons.plotting_boxplot")
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
    
    # Note: In the new logic, we iterate over samples, but plotting_amplicons 
    # might not call savefig if 'bam' isn't in the columns or index. 
    # With the logic provided previously, it should work.