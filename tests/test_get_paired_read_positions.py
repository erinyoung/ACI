import os
import pytest
import pandas as pd
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
    df = get_paired_read_positions(bam_path, bed_trees)

    # Basic structure checks
    assert not df.empty
    assert all(
        col in df.columns
        for col in ["read_name", "chrom", "read_start", "read_end", "amplicon", "bam"]
    )

    # Optional: check for known overlap
    expected_amplicons = {"52"}
    assert set(df["amplicon"]) <= expected_amplicons
