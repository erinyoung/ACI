import os
import pandas as pd
import pytest
from unittest import mock

from aci.utils.read_and_assign import read_and_assign


def test_read_and_assign(tmp_path):
    bam_path = "/fake/path/sample.bam"
    bed_trees = {"chr1": "fake_interval_tree"}
    temp_dir = tmp_path.as_posix()

    # Mock return DataFrame for paired and unpaired
    paired_df = pd.DataFrame(
        {
            "read_name": ["read1"],
            "chrom": ["chr1"],
            "read_start": [100],
            "read_end": [150],
            "amplicon": ["amp1"],
            "bam": ["sample.bam"],
        }
    )
    unpaired_df = pd.DataFrame(
        {
            "read_name": ["read2"],
            "chrom": ["chr1"],
            "read_start": [200],
            "read_end": [250],
            "amplicon": ["amp2"],
            "bam": ["sample.bam"],
        }
    )

    with mock.patch(
        "aci.utils.read_and_assign.is_paired_bam", return_value=True
    ) as mock_paired, mock.patch(
        "aci.utils.read_and_assign.get_paired_read_positions", return_value=paired_df
    ) as mock_get_paired, mock.patch(
        "aci.utils.read_and_assign.get_unpaired_read_positions",
        return_value=unpaired_df,
    ) as mock_get_unpaired, mock.patch(
        "pandas.DataFrame.to_csv"
    ) as mock_to_csv:

        # Case 1: Paired BAM
        assigned_file = read_and_assign(bam_path, bed_trees, temp_dir)
        mock_paired.assert_called_once_with(bam_path)
        mock_get_paired.assert_called_once_with(bam_path, bed_trees)
        mock_get_unpaired.assert_not_called()
        mock_to_csv.assert_called_once()
        assert os.path.basename(bam_path) in assigned_file
        mock_to_csv.reset_mock()
        mock_paired.reset_mock()
        mock_get_paired.reset_mock()
        mock_get_unpaired.reset_mock()

        # Case 2: Unpaired BAM
        mock_paired.return_value = False
        assigned_file = read_and_assign(bam_path, bed_trees, temp_dir)
        mock_paired.assert_called_once_with(bam_path)
        mock_get_unpaired.assert_called_once_with(bam_path, bed_trees)
        mock_get_paired.assert_not_called()
        mock_to_csv.assert_called_once()
