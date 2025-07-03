import pytest
from unittest import mock
from aci.utils.is_paired import is_paired_bam

class MockRead:
    def __init__(self, is_paired):
        self.is_paired = is_paired

class MockAlignmentFile:
    def __init__(self, reads):
        self.reads = reads
        self.index = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __iter__(self):
        return iter(self.reads)

def test_is_paired_bam_returns_true_for_paired_reads():
    # Create mock reads: one paired read among the first 1000
    reads = [MockRead(is_paired=False)] * 10 + [MockRead(is_paired=True)] + [MockRead(is_paired=False)] * 10
    with mock.patch("aci.utils.get_coverage.pysam.AlignmentFile", return_value=MockAlignmentFile(reads)):
        result = is_paired_bam("fake.bam")
    assert result is True

def test_is_paired_bam_returns_false_if_no_paired_reads():
    reads = [MockRead(is_paired=False)] * 1001  # all unpaired
    with mock.patch("aci.utils.get_coverage.pysam.AlignmentFile", return_value=MockAlignmentFile(reads)):
        result = is_paired_bam("fake.bam")
    assert result is False
