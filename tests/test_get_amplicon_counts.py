import pandas as pd
import pytest

from aci.utils.get_amplicon_counts import get_amplicon_counts


@pytest.fixture
def create_interval_files(tmp_path):
    # Create first fake interval file
    df1 = pd.DataFrame(
        {
            "bam": ["sample1.bam", "sample1.bam", "sample1.bam", "sample2.bam"],
            "amplicon": ["amp1", "amp1", "amp2", "amp1"],
            "read_name": ["read1", "read2", "read1", "read3"],
        }
    )
    file1 = tmp_path / "interval1.csv"
    df1.to_csv(file1, index=False)

    # Create second fake interval file
    df2 = pd.DataFrame(
        {
            "bam": ["sample2.bam", "sample2.bam", "sample3.bam"],
            "amplicon": ["amp1", "amp2", "amp2"],
            "read_name": ["read4", "read5", "read6"],
        }
    )
    file2 = tmp_path / "interval2.csv"
    df2.to_csv(file2, index=False)

    return [str(file1), str(file2)]


def test_get_amplicon_counts(create_interval_files):
    amplicon_names = ["amp1", "amp2"]

    max_df, min_df = get_amplicon_counts(create_interval_files, amplicon_names)

    expected_cols = ["bam"] + amplicon_names
    assert list(max_df.columns) == expected_cols
    assert list(min_df.columns) == expected_cols

    # Group and sum counts per bam (since concat may have multiple rows per bam)
    max_counts_by_bam = max_df.groupby("bam")[amplicon_names].sum()
    min_counts_by_bam = min_df.groupby("bam")[amplicon_names].sum()

    assert max_counts_by_bam.loc["sample1.bam", "amp1"] == 2
    assert max_counts_by_bam.loc["sample1.bam", "amp2"] == 1

    assert min_counts_by_bam.loc["sample1.bam", "amp1"] == 1
    assert min_counts_by_bam.loc["sample2.bam", "amp2"] == 1  # This now should pass

    assert "sample3.bam" in max_counts_by_bam.index
    assert "sample3.bam" in min_counts_by_bam.index
