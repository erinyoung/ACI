import pytest
from unittest import mock
from types import SimpleNamespace

from aci.utils.process_bams_in_parallel import process_bams_in_parallel


@mock.patch("aci.utils.process_bams_in_parallel.as_completed")
@mock.patch("aci.utils.process_bams_in_parallel.read_and_assign")
@mock.patch("aci.utils.process_bams_in_parallel.divide_chrom_by_span")
def test_process_bams_in_parallel(mock_divide_chrom, mock_read_assign, mock_as_completed):
    # Setup input
    bam_files = ["bam1.bam", "bam2.bam"]
    bed_intervals = {"chr1": "fake_interval_tree"}
    temp_dir = "/tmp"
    args = SimpleNamespace(threads=2)

    # Mock the region division
    mock_divide_chrom.return_value = ["chr1:0:1000", "chr1:1000:2000"]

    # Prepare mock futures
    mock_futures = []
    results = ["file1.csv", "file2.csv", "file3.csv", "file4.csv"]
    for result in results:
        future = mock.Mock()
        future.result.return_value = result
        mock_futures.append(future)

    # read_and_assign is used in submit, so just patch as_completed to simulate results
    mock_as_completed.return_value = mock_futures

    # Execute function
    output = process_bams_in_parallel(bam_files, bed_intervals, args, temp_dir)

    # Verify expected output
    assert output == results

    # Validate call count
    assert mock_read_assign.call_count == 0  # because it's not actually called; it's submitted

    # Optionally check if the submit calls were correct:
    expected_tasks = [
        mock.call("bam1.bam", bed_intervals, "chr1:0:1000", temp_dir),
        mock.call("bam1.bam", bed_intervals, "chr1:1000:2000", temp_dir),
        mock.call("bam2.bam", bed_intervals, "chr1:0:1000", temp_dir),
        mock.call("bam2.bam", bed_intervals, "chr1:1000:2000", temp_dir),
    ]

    # To test this, patch ProcessPoolExecutor.submit directly
    with mock.patch("aci.utils.process_bams_in_parallel.ProcessPoolExecutor") as mock_executor_cls:
        mock_executor = mock_executor_cls.return_value.__enter__.return_value
        mock_executor.submit.side_effect = mock_futures

        # Run again to check submit call args
        process_bams_in_parallel(bam_files, bed_intervals, args, temp_dir)

        submit_calls = mock_executor.submit.call_args_list

        expected_tasks = [
            mock.call(mock_read_assign, "bam1.bam", bed_intervals, "chr1:0:1000", temp_dir),
            mock.call(mock_read_assign, "bam1.bam", bed_intervals, "chr1:1000:2000", temp_dir),
            mock.call(mock_read_assign, "bam2.bam", bed_intervals, "chr1:0:1000", temp_dir),
            mock.call(mock_read_assign, "bam2.bam", bed_intervals, "chr1:1000:2000", temp_dir),
        ]
        for expected_call in expected_tasks:
            assert expected_call in submit_calls

