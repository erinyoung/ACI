import pytest
import pandas as pd
from unittest import mock
import sys

from aci.utils.split_dataframe import split_dataframe


def test_split_dataframe_normal():
    # Sample input DataFrame
    df = pd.DataFrame(
        {
            "bam": ["sample1.bam", "sample2.bam", "sample1.bam"],
            "pos": [100, 600, 1100],
            "ref": ["chr1", "chr1", "chr1"],
            "cov": [10, 20, 15],
        }
    )

    # Mock group_create to just return a simple DataFrame
    with mock.patch(
        "aci.utils.split_dataframe.group_create"
    ) as mock_group_create, mock.patch(
        "aci.utils.split_dataframe.group_mean"
    ) as mock_group_mean:

        mock_group_create.return_value = pd.DataFrame(
            {"pos": ["0-499", "500-999", "1000-1499"], "group": [0, 1, 2]}
        )

        # Mock group_mean to return a DataFrame with group and coverage columns
        mock_group_mean.side_effect = lambda df, name: pd.DataFrame(
            {"group": [0, 1, 2], name: [5, 10, 15]}
        )

        result = split_dataframe(df)

        # Check the returned DataFrame has expected columns (group + each bam)
        expected_columns = {"pos", "group", "sample1.bam", "sample2.bam"}
        assert set(result.columns) == expected_columns

        # Check the pos column has correct bin strings
        assert all(s in ["0-499", "500-999", "1000-1499"] for s in result["pos"])


def test_split_dataframe_multiple_references(monkeypatch):
    # Input DataFrame with multiple references
    df = pd.DataFrame(
        {
            "bam": ["sample1.bam", "sample2.bam"],
            "pos": [100, 200],
            "ref": ["chr1", "chr2"],
            "cov": [10, 20],
        }
    )

    # Patch sys.exit to raise SystemExit so we can catch it
    with pytest.raises(SystemExit):
        split_dataframe(df)
