import os
import pytest
from aci.logic.counter import count_amplicons_in_bam
from aci.logic.bed_parser import parse_bed

# Paths
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
BAM_FILE = os.path.join(TEST_DATA_DIR, "test.bam")
BED_FILE = os.path.join(TEST_DATA_DIR, "test.bed")

def test_bed_parser():
    """Verify we can parse the test.bed file correctly."""
    amplicons = parse_bed(BED_FILE)
    
    assert len(amplicons) > 0
    first_amp = amplicons[0]
    
    # Verify structure
    assert 'chrom' in first_amp
    assert 'start' in first_amp
    assert 'end' in first_amp
    assert 'name' in first_amp
    
    # Verify types
    assert isinstance(first_amp['start'], int)
    assert isinstance(first_amp['end'], int)

def test_counter_logic_on_real_bam():
    """
    Run the core counting logic on test.bam.
    Verify the invariant: Max Depth (Overlap) >= Min Depth (Strict).
    """
    amplicons = parse_bed(BED_FILE)
    
    # UNPACK TUPLE HERE: (counts, reads)
    results, read_assignments = count_amplicons_in_bam(BAM_FILE, amplicons)
    
    assert len(results) > 0
    
    # Optional: Verify read assignments were returned
    # (The test.bam might be small, but it should return a list)
    assert isinstance(read_assignments, list)
    
    for row in results:
        max_c = row['max_count']
        min_c = row['min_count']
        
        # Invariant: It is impossible for Strict Count to be higher than Overlap Count
        assert max_c >= min_c, (
            f"Logic Error for amplicon {row['amplicon']}: "
            f"Min ({min_c}) > Max ({max_c})"
        )
        
        # Sanity check: Counts should be non-negative
        assert max_c >= 0
        assert min_c >= 0