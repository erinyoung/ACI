import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import pytest
from unittest import mock
import pandas as pd

from aci.utils.process_bams_in_parallel import process_bams_in_parallel

def test_process_bams_in_parallel():
    bam_files = ["bam1.bam", "bam2.bam"]
    bed_intervals = {"chr1": "fake_interval_tree"}
    temp_dir = "/tmp"

    df1 = pd.DataFrame({"a": [1, 2]})
    df2 = pd.DataFrame({"a": [3, 4]})

    with mock.patch("aci.utils.process_bams_in_parallel.read_and_assign") as mock_read_assign, \
         mock.patch("concurrent.futures.ProcessPoolExecutor", new=ThreadPoolExecutor):

        mock_read_assign.side_effect = [df1, df2]

        results = process_bams_in_parallel(bam_files, bed_intervals, temp_dir)

        # Now read_and_assign *should* be called inside the same process
        mock_read_assign.assert_any_call("bam1.bam", bed_intervals, temp_dir)
        mock_read_assign.assert_any_call("bam2.bam", bed_intervals, temp_dir)

        assert len(results) == 2
        assert any(df1.equals(df) for df in results)
        assert any(df2.equals(df) for df in results)

