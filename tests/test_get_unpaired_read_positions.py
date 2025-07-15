import pandas as pd
import pytest
from unittest import mock
from types import SimpleNamespace
from aci.utils.get_unpaired_read_positions import get_unpaired_read_positions


class MockInterval:
    def __init__(self, data):
        self.data = data


class MockIntervalTree:
    def overlap(self, start, end):
        # Return dummy intervals for overlap
        return [MockInterval("ampliconX"), MockInterval("ampliconY")]


@pytest.fixture
def mock_reads():
    # Create mock reads with required attributes
    read1 = SimpleNamespace(
        query_name="read1",
        is_secondary=False,
        is_supplementary=False,
        is_unmapped=False,
        reference_name="chr1",
        reference_start=100,
        reference_end=150,
    )
    read2 = SimpleNamespace(
        query_name="read2",
        is_secondary=False,
        is_supplementary=False,
        is_unmapped=False,
        reference_name="chr1",
        reference_start=200,
        reference_end=250,
    )
    read3 = SimpleNamespace(
        query_name="read3",
        is_secondary=True,  # should be skipped
        is_supplementary=False,
        is_unmapped=False,
        reference_name="chr1",
        reference_start=300,
        reference_end=350,
    )
    read4 = SimpleNamespace(
        query_name="read4",
        is_secondary=False,
        is_supplementary=True,  # should be skipped
        is_unmapped=False,
        reference_name="chr1",
        reference_start=400,
        reference_end=450,
    )
    read5 = SimpleNamespace(
        query_name="read5",
        is_secondary=False,
        is_supplementary=False,
        is_unmapped=True,  # should be skipped
        reference_name="chr1",
        reference_start=500,
        reference_end=550,
    )
    return [read1, read2, read3, read4, read5]


def test_get_unpaired_read_positions(monkeypatch, mock_reads):
    bed_trees = {"chr1": MockIntervalTree()}
    bam_path = "/path/to/sample.bam"

    mock_alignment_file = mock.MagicMock()
    mock_alignment_file.fetch.return_value = iter(mock_reads)
    mock_alignment_file.close.return_value = None

    monkeypatch.setattr(
        "aci.utils.get_unpaired_read_positions.pysam.AlignmentFile",
        lambda path, mode: mock_alignment_file,
    )

    df = get_unpaired_read_positions(bam_path, bed_trees)

    # Check dataframe columns
    assert set(df.columns) == {
        "read_name",
        "chrom",
        "read_start",
        "read_end",
        "amplicon",
        "bam",
    }

    # Check bam basename
    assert all(df["bam"] == "sample.bam")

    # Should contain read1 and read2 only (others skipped)
    assert set(df["read_name"]) == {"read1", "read2"}

    # Each read should produce two rows (for the two intervals in overlap)
    assert len(df) == 4

    # Check amplicon values
    expected_amplicons = {"ampliconX", "ampliconY"}
    assert set(df["amplicon"]) == expected_amplicons
