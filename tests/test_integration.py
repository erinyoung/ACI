import os
import shutil
import subprocess
import pytest
import pandas as pd

# Paths to your existing test data
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
BAM_FILE = os.path.join(TEST_DATA_DIR, "test.bam")
BED_FILE = os.path.join(TEST_DATA_DIR, "test.bed")
OUT_DIR = os.path.join(os.path.dirname(__file__), "output_test")

@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    """Ensure output directory is clean before and after tests."""
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)
    yield
    # Comment out next line if you want to inspect output after tests
    shutil.rmtree(OUT_DIR)

def test_aci_cli_end_to_end():
    """
    Runs the ACI CLI against the real test.bam and test.bed.
    """
    cmd = [
        "python", "-m", "aci.cli", 
        "-b", BAM_FILE,
        "-d", BED_FILE,
        "-o", OUT_DIR,
        "-t", "2"
    ]
    
    # Run the command
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    assert result.returncode == 0, f"ACI failed with error:\n{result.stderr}"

    # Check for ALL output files (Old + New)
    expected_files = [
        "amplicon_max_depth.csv",
        "amplicon_min_depth.csv",
        "amplicon_read_assignments.csv",
        "amplicon_max_depth_boxplot.png",
        "amplicon_min_depth_boxplot.png",
        "overall_depth.csv",
        
        # --- NEW FILES ---
        "heatmap_max_depth.png",
        "heatmap_min_depth.png",
        "heatmap_efficiency.png",       # New Heatmap
        "dropout_report.tsv",           # New Report
        "sample_uniformity_report.tsv", # New Report
        "amplicon_efficiency_matrix.csv" # New Report
    ]
    
    for fname in expected_files:
        fpath = os.path.join(OUT_DIR, fname)
        assert os.path.exists(fpath), f"Missing expected output file: {fname}"

    # Verify Masking Directory
    mask_dir = os.path.join(OUT_DIR, "masking_files")
    assert os.path.exists(mask_dir)
    assert len(os.listdir(mask_dir)) > 0

    # Quick Data Check
    eff_df = pd.read_csv(os.path.join(OUT_DIR, "amplicon_efficiency_matrix.csv"))
    assert not eff_df.empty