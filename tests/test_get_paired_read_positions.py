import pandas as pd
import pytest
from unittest import mock
from types import SimpleNamespace
from aci.utils.get_paired_read_positions import get_paired_read_positions  # update to your actual module path

def make_mock_read(query_name, is_proper_pair=True, is_secondary=False, is_supplementary=False,
                   is_read1=False, reference_name="chr1", reference_start=0, reference_end=10):
    read = SimpleNamespace()
    read.query_name = query_name
    read.is_proper_pair = is_proper_pair
    read.is_secondary = is_secondary
    read.is_supplementary = is_supplementary
    read.is_read1 = is_read1
    read.reference_name = reference_name
    read.reference_start = reference_start
    read.reference_end = reference_end
    return read

class MockInterval:
    def __init__(self, data):
        self.data = data

class MockIntervalTree:
    def overlap(self, start, end):
        # Return some dummy intervals overlapping
        return [MockInterval("amplicon1"), MockInterval("amplicon2")]

@pytest.fixture
def mock_bam():
    # Create two reads from the same pair with overlapping names
    read1 = make_mock_read("readA", is_read1=True, reference_start=100, reference_end=150)
    read2 = make_mock_read("readA", is_read1=False, reference_start=120, reference_end=170)

    read3 = make_mock_read("readB", is_read1=True, reference_start=200, reference_end=250)
    read4 = make_mock_read("readC", is_read1=True, reference_start=300, reference_end=350)  # Different name to test skipping

    # Mock fetch to return these reads in order
    return [read1, read2, read3, read4]

def test_get_paired_read_positions(monkeypatch, mock_bam):
    bed_trees = {"chr1": MockIntervalTree()}
    bam_path = "/fake/path/sample.bam"

    # Mock pysam.AlignmentFile to return an object whose fetch returns our mock reads
    mock_alignment_file = mock.MagicMock()
    mock_alignment_file.fetch.return_value = iter(mock_bam)
    mock_alignment_file.close.return_value = None

    monkeypatch.setattr("aci.utils.get_paired_read_positions.pysam.AlignmentFile", lambda path, mode: mock_alignment_file)

    df = get_paired_read_positions(bam_path, bed_trees)

    # Check dataframe columns
    assert set(df.columns) == {"read_name", "chrom", "read_start", "read_end", "amplicon", "bam"}

    # Check that bam basename is used
    assert all(df["bam"] == "sample.bam")

    # Check read names and amplicons are correct
    # For readA (paired), expect two intervals amplicon1 and amplicon2
    readA_rows = df[df["read_name"] == "readA"]
    assert set(readA_rows["amplicon"]) == {"amplicon1", "amplicon2"}
    assert readA_rows["chrom"].iloc[0] == "chr1"
    assert readA_rows["read_start"].iloc[0] == 100
    assert readA_rows["read_end"].iloc[0] == 170

    # readB and readC have no pair, so should be skipped
    assert "readB" not in df["read_name"].values
    assert "readC" not in df["read_name"].values

