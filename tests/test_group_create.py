import pandas as pd
import pytest
from unittest import mock
from types import SimpleNamespace
from aci.utils.group_create import group_create


def test_group_create():
    positions = [0, 499, 500, 999, 1000, 1500, 1501, 2000]

    result_df = group_create(positions)

    # Expected groups for each position
    expected_groups = {
        "0-499": 0,
        "500-999": 1,
        "1000-1499": 2,
        "1500-1999": 3,
        "2000-2499": 4,
    }

    # Check the returned DataFrame has expected shape and columns
    assert list(result_df.columns) == ["pos", "group"]
    assert len(result_df) == len(expected_groups)

    # Check each pos string and corresponding group
    for _, row in result_df.iterrows():
        assert row["pos"] in expected_groups
        assert row["group"] == expected_groups[row["pos"]]

    # Check group column is integer type
    assert pd.api.types.is_integer_dtype(result_df["group"])
