import pytest
import pandas as pd
from unittest import mock
from aci.logic.genome_depth import genome_depth

def test_genome_depth():
    mock_depth_output = "chr1\t1\t10\n" "chr1\t2\t15\n" "chr1\t3\t20\n"

    # CHANGED: aci.utils -> aci.logic
    with mock.patch(
        "aci.logic.genome_depth.pysam.depth", return_value=mock_depth_output
    ):
        df = genome_depth("tests/data/test.bam")
        print(df)

    assert list(df.columns) == ["ref", "pos", "cov", "bam"]
    assert df["ref"].tolist() == ["chr1", "chr1", "chr1"]
    assert df["pos"].tolist() == [1, 2, 3]
    assert df["cov"].tolist() == [10, 15, 20]
    assert pd.api.types.is_numeric_dtype(df["pos"])
    assert pd.api.types.is_numeric_dtype(df["cov"])