import pandas as pd
import pytest
from unittest import mock
from aci.utils.plotting_depth import plotting_depth

def test_plotting_depth(tmp_path):
    # Sample DataFrame returned by split_dataframe
    sample_df = pd.DataFrame({
        "pos": [0, 500, 1000],
        "group": [0, 1, 2],
        "cov": [10, 20, 30]
    })

    # Patch split_dataframe and plotting_boxplot
    with mock.patch("aci.utils.plotting_depth.split_dataframe", return_value=sample_df) as mock_split, \
         mock.patch("aci.utils.plotting_depth.plotting_boxplot") as mock_plotbox:

        out_dir = tmp_path

        # Call function under test
        plotting_depth(sample_df, str(out_dir))

        # Assert split_dataframe called once with original df
        mock_split.assert_called_once_with(sample_df)

        # Check CSV file is created and content matches expected columns
        csv_file = out_dir / "overall_depth.csv"
        assert csv_file.exists()

        df_read = pd.read_csv(csv_file)
        assert list(df_read.columns) == ["pos", "group", "cov"]

        # Prepare expected DataFrame passed to plotting_boxplot
        expected_df = sample_df.copy()
        expected_df["ungroup"] = expected_df["group"] * 500
        expected_df = expected_df.drop(columns=["pos", "group"]).set_index("ungroup").transpose()

        # Check plotting_boxplot called once
        mock_plotbox.assert_called_once()
        args, kwargs = mock_plotbox.call_args

        # First arg to plotting_boxplot should be expected_df (check dataframe equality)
        pd.testing.assert_frame_equal(args[0], expected_df)

        # Second arg should be the dictionary with keys and correct filename
        plot_params = args[1]
        assert plot_params["title"] == "Overall coverage"
        assert plot_params["ylabel"] == "meandepth"
        assert plot_params["xlabel"] == "position"
        assert plot_params["file"] == f"{out_dir}/overall_depth.png"
