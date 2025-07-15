import os
import pandas as pd
import pytest
from unittest import mock

from intervaltree import IntervalTree, Interval
from aci.utils.read_and_assign import read_and_assign


def test_read_and_assign(tmp_path):
    bam_path = "tests/data/test.bam"
    bed_trees = {
        'MN908947.3': IntervalTree([
            Interval(1264, 1623, '5'),
            Interval(1595, 1942, '6'),
            Interval(1897, 2242, '7'),
            Interval(14895, 15224, '50'),
            Interval(15193, 15538, '51'),
            Interval(15503, 15861, '52'),
            Interval(15851, 16186, '53'),
            Interval(16144, 16485, '54'),
            Interval(27808, 28145, '92'),
            Interval(28104, 28442, '93'),
            Interval(28416, 28756, '94'),
            Interval(28699, 29041, '95'),
            Interval(29007, 29356, '96')
        ])
    }
    region = "MN908947.3:1264:1623"  # Use a single region string
    temp_dir = tmp_path.as_posix()

    # Mock DataFrames
    paired_df = pd.DataFrame({
        "read_name": ["read1"],
        "chrom": ["MN908947.3"],
        "read_start": [14995],
        "read_end": [15146],
        "amplicon": ["amp1"],
        "bam": ["test.bam"],
    })
    unpaired_df = pd.DataFrame({
        "read_name": ["read2"],
        "chrom": ["MN908947.3"],
        "read_start": [15295],
        "read_end": [15446],
        "amplicon": ["amp2"],
        "bam": ["test.bam"],
    })

    with mock.patch("aci.utils.read_and_assign.is_paired_bam", return_value=True) as mock_paired, \
         mock.patch("aci.utils.read_and_assign.get_paired_read_positions", return_value=paired_df) as mock_get_paired, \
         mock.patch("aci.utils.read_and_assign.get_unpaired_read_positions", return_value=unpaired_df) as mock_get_unpaired:

        # Case 1: Paired
        assigned_file = read_and_assign(bam_path, bed_trees, region, temp_dir)
        mock_paired.assert_called_once_with(bam_path)
        mock_get_paired.assert_called_once_with(bam_path, bed_trees, region)
        mock_get_unpaired.assert_not_called()
        assert assigned_file.endswith(".csv")
        assert os.path.basename(bam_path) in assigned_file

        # Reset mocks
        mock_paired.reset_mock()
        mock_get_paired.reset_mock()
        mock_get_unpaired.reset_mock()

        # Case 2: Unpaired
        mock_paired.return_value = False
        assigned_file = read_and_assign(bam_path, bed_trees, region, temp_dir)
        mock_paired.assert_called_once_with(bam_path)
        mock_get_unpaired.assert_called_once_with(bam_path, bed_trees)
        mock_get_paired.assert_not_called()
        assert assigned_file.endswith(".csv")
        assert os.path.basename(bam_path) in assigned_file
