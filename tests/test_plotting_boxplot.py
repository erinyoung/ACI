import pandas as pd
import pytest
from unittest import mock
import matplotlib.pyplot as plt
from aci.utils.plotting_boxplot import plotting_boxplot


def test_plotting_boxplot():
    # Create sample dataframe with numeric columns
    df = pd.DataFrame({"amp1": [1, 2, 3, 4, 5], "amp2": [5, 6, 7, 8, 9]})

    plot_params = {
        "title": "Test Title",
        "ylabel": "Y Label",
        "xlabel": "X Label",
        "file": "test_plot.png",
    }

    with mock.patch.object(plt.Figure, "savefig") as mock_savefig, mock.patch(
        "matplotlib.pyplot.close"
    ) as mock_close:

        plotting_boxplot(df, plot_params)

        # Check savefig called with correct filename and bbox_inches
        mock_savefig.assert_called_once_with("test_plot.png", bbox_inches="tight")

        # Check close called to close the figure
        mock_close.assert_called_once()
