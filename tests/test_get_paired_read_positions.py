import os
import pytest
import pandas as pd
import pysam
from intervaltree import IntervalTree, Interval
from aci.utils.get_paired_read_positions import get_paired_read_positions


@pytest.fixture
def bam_path():
    """Path to test BAM file"""
    return "tests/data/test.bam"


@pytest.fixture
def bed_trees():
    """Mock BED interval tree matching regions in test BAM"""
    trees = {
        "MN908947.3": IntervalTree(
            [
                Interval(15503, 15861, "52"),  # overlaps read
                Interval(29007, 29356, "96"),  # doesn't
            ]
        )
    }
    return trees


def test_get_paired_read_positions_with_real_bam(bam_path, bed_trees):
    # Provide a region that matches the known reads in your BAM file
    region = "MN908947.3:15500:15900"
    pysam.index(bam_path)
    df = get_paired_read_positions(bam_path, bed_trees, region)

    assert not df.empty
    assert set(df.columns) == {
        "read_name", "chrom", "read_start", "read_end", "amplicon", "bam"
    }

    # Optional: ensure assigned amplicons are expected
    expected_amplicons = {"52"}
    assert set(df["amplicon"]).issubset(expected_amplicons)
