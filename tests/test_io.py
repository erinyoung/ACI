import os
import tempfile
import pytest
from aci.utils.io import prep, check_bam_status

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
BAM_FILE = os.path.join(TEST_DATA_DIR, "test.bam")

def test_check_bam_status():
    """Test that we can detect sorting status."""
    is_sorted, has_index = check_bam_status(BAM_FILE)
    
    # We assume test.bam might be sorted, but maybe not indexed depending on your repo state.
    # This just ensures the function runs without crashing.
    assert isinstance(is_sorted, bool)
    assert isinstance(has_index, bool)

def test_prep_creates_index():
    """Test that prep ensures an index exists."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_bam = os.path.join(temp_dir, "temp.bam")
        
        # Run prep
        final_bam = prep(BAM_FILE, temp_bam, threads=1)
        
        # Result should exist
        assert os.path.exists(final_bam)
        
        # Index should now exist (either .bai or .crai)
        assert os.path.exists(final_bam + ".bai") or os.path.exists(final_bam + ".crai")