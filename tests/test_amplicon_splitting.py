import pytest
from unittest import mock
from types import SimpleNamespace
import pandas as pd
from intervaltree import IntervalTree, Interval

from aci.utils.amplicon_splitting import amplicon_splitting

@mock.patch("aci.utils.amplicon_splitting.get_amplicon_counts")
@mock.patch("aci.utils.amplicon_splitting.process_bams_in_parallel")
@mock.patch("aci.utils.amplicon_splitting.load_bed_intervals")
def test_amplicon_splitting(mock_load_bed_intervals,
                             mock_process_bams,
                             mock_get_counts):

    # Fake data
    bed_trees = {'MN908947.3': IntervalTree([Interval(1264, 1623, '5'), Interval(1595, 1942, '6'), Interval(1897, 2242, '7'), Interval(14895, 15224, '50'), Interval(15193, 15538, '51'), Interval(15503, 15861, '52'), Interval(15851, 16186, '53'), Interval(16144, 16485, '54'), Interval(27808, 28145, '92'), Interval(28104, 28442, '93'), Interval(28416, 28756, '94'), Interval(28699, 29041, '95'), Interval(29007, 29356, '96')])}
    amplicon_names = ['5', '6', '7', '50', '51', '52', '53', '54', '92', '93', '94', '95', '96']
    mock_load_bed_intervals.return_value = (bed_trees, amplicon_names)

    interval_files = ["tests/data/test.interval.csv"]
    mock_process_bams.return_value = interval_files

    # Mock pandas DataFrames
    max_df = pd.DataFrame({"1": [1], "2": [2]})
    min_df = pd.DataFrame({"1": [0.5], "2": [1.5]})
    mock_get_counts.return_value = (max_df, min_df)

    # Fake input args
    meta = {"tmp": "/tmp/"}
    args = SimpleNamespace(bam=["tests/data/test.bam"], bed="tests/data/test.bed")

    result_max, result_min = amplicon_splitting(meta, args)

    # Assertions
    mock_load_bed_intervals.assert_called_once_with("tests/data/test.bed")
    mock_process_bams.assert_called_once_with(["tests/data/test.bam"], bed_trees, "/tmp/")
    mock_get_counts.assert_called_once_with(interval_files, amplicon_names)

    pd.testing.assert_frame_equal(result_max, max_df)
    pd.testing.assert_frame_equal(result_min, min_df)
