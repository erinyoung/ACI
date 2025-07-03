import os
from unittest import mock
from aci.utils.prep import prep 

def test_prep_calls_sort_and_index():
    initial = "tests/data/test.bam"
    final = "tests/data/test_sorted.bam"
    threads = 4

    # Patch os.path.exists to simulate files existing
    with mock.patch("os.path.exists") as mock_exists, \
         mock.patch("pysam.sort") as mock_sort, \
         mock.patch("pysam.index") as mock_index:

        # Simulate that initial and final BAM files exist
        def exists_side_effect(path):
            if path == initial:
                return True
            if path == final:
                return True
            return False

        mock_exists.side_effect = exists_side_effect

        # Call function
        prep(initial, final, threads)

        # Assert pysam.sort was called with expected arguments
        mock_sort.assert_called_once_with("-o", final, "-@", str(threads), initial)

        # Assert pysam.index was called on final bam
        mock_index.assert_called_once_with(final)

def test_prep_skips_sort_if_initial_missing():
    initial = "nonexistent.bam"
    final = "tests/data/test_sorted.bam"
    threads = 4

    with mock.patch("os.path.exists") as mock_exists, \
         mock.patch("pysam.sort") as mock_sort, \
         mock.patch("pysam.index") as mock_index:

        # Simulate initial file does not exist but final does
        def exists_side_effect(path):
            if path == initial:
                return False
            if path == final:
                return True
            return False

        mock_exists.side_effect = exists_side_effect

        prep(initial, final, threads)

        # pysam.sort should NOT be called
        mock_sort.assert_not_called()

        # pysam.index should still be called (because final exists)
        mock_index.assert_called_once_with(final)
