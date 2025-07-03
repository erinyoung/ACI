import pytest
from unittest import mock
from aci.utils.get_coverage import get_coverage  # adjust import path

def test_get_coverage_file_exists_and_not_exists():
    bam_path = "fake.bam"
    subrange = "chr1:100-200"

    # Mock for os.path.exists to simulate BAM file presence
    with mock.patch("aci.utils.get_coverage.os.path.exists", return_value=True), \
         mock.patch("aci.utils.get_coverage.pysam.coverage", return_value="some output 0 0 0 0 30.5 rest") as mock_coverage:
        
        cov = get_coverage(bam_path, subrange)
        
        # Ensure pysam.coverage was called with correct arguments
        mock_coverage.assert_called_once_with("--no-header", bam_path, "-r", subrange)
        
        # The 7th element (index 6) is 30.5 in the mocked output -> float conversion
        assert cov == 30.5

    # Test when file does not exist, coverage should be 0.0
    with mock.patch("aci.utils.get_coverage.os.path.exists", return_value=False):
        cov = get_coverage(bam_path, subrange)
        assert cov == 0.0
