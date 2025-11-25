import pytest
from unittest import mock
from aci.logic.get_coverage import get_coverage

def test_get_coverage_file_exists_and_not_exists():
    bam_path = "fake.bam"
    subrange = "chr1:100-200"

    # CHANGED: aci.utils -> aci.logic (for both patches)
    with mock.patch(
        "aci.logic.get_coverage.os.path.exists", return_value=True
    ), mock.patch(
        "aci.logic.get_coverage.pysam.coverage",
        return_value="some output 0 0 0 0 30.5 rest",
    ) as mock_coverage:

        cov = get_coverage(bam_path, subrange)

        # Ensure pysam.coverage was called with correct arguments
        mock_coverage.assert_called_once_with("--no-header", bam_path, "-r", subrange)

        # The 7th element (index 6) is 30.5 in the mocked output -> float conversion
        assert cov == 30.5

    # CHANGED: aci.utils -> aci.logic
    with mock.patch("aci.logic.get_coverage.os.path.exists", return_value=False):
        cov = get_coverage(bam_path, subrange)
        assert cov == 0.0