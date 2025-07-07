import pytest
from unittest import mock
from intervaltree import IntervalTree
from aci.utils.load_bed_intervals import load_bed_intervals


def test_load_bed_intervals_success(tmp_path):
    # Create a temporary BED file with valid lines
    bed_content = """chr1\t100\t200\tamp1
chr1\t300\t400\tamp2
chr2\t500\t600\tamp3
"""
    bed_file = tmp_path / "test.bed"
    bed_file.write_text(bed_content)

    trees, names = load_bed_intervals(str(bed_file))

    # Check keys and names
    assert set(trees.keys()) == {"chr1", "chr2"}
    assert names == ["amp1", "amp2", "amp3"]

    # Check IntervalTree contents for chr1
    intervals_chr1 = sorted(trees["chr1"])
    assert intervals_chr1[0].begin == 100
    assert intervals_chr1[0].end == 200
    assert intervals_chr1[0].data == "amp1"
    assert intervals_chr1[1].data == "amp2"


def test_load_bed_intervals_missing_columns(tmp_path):
    # BED line with less than 4 columns
    bed_content = "chr1\t100\t200\n"
    bed_file = tmp_path / "bad_columns.bed"
    bed_file.write_text(bed_content)

    with pytest.raises(SystemExit):
        load_bed_intervals(str(bed_file))


def test_load_bed_intervals_duplicate_names(tmp_path):
    # Duplicate amplicon names
    bed_content = """chr1\t100\t200\tamp1
chr1\t300\t400\tamp1
"""
    bed_file = tmp_path / "dup_names.bed"
    bed_file.write_text(bed_content)

    with pytest.raises(SystemExit):
        load_bed_intervals(str(bed_file))
