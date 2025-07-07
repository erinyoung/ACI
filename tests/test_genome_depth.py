import pytest
import pandas as pd
from unittest import mock

from aci.utils.genome_depth import genome_depth


def test_genome_depth():

    mock_depth_output = "chr1\t1\t10\n" "chr1\t2\t15\n" "chr1\t3\t20\n"

    meta = {"sorted_bam": "fake.bam", "file_name": "fake.bam"}

    # Patch pysam.depth at the module where genome_depth is defined
    with mock.patch(
        "aci.utils.genome_depth.pysam.depth", return_value=mock_depth_output
    ):

        df = genome_depth(meta)

    assert list(df.columns) == ["ref", "pos", "cov", "bam"]
    assert df["ref"].tolist() == ["chr1", "chr1", "chr1"]
    assert df["pos"].tolist() == [1, 2, 3]
    assert df["cov"].tolist() == [10, 15, 20]
    assert all(df["bam"] == "fake.bam")
    assert pd.api.types.is_numeric_dtype(df["pos"])
    assert pd.api.types.is_numeric_dtype(df["cov"])
