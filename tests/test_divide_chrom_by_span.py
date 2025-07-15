import pytest
from collections import namedtuple
from aci.utils.divide_chrom_by_span import divide_chrom_by_span

# Define a simple Interval class to mimic bed intervals
Interval = namedtuple("Interval", ["begin", "end"])

def test_divide_chrom_by_span_basic():
    # Setup: mimic bed_trees as {chrom: list_of_intervals}
    bed_trees = {
        "chr1": [
            Interval(0, 100),
            Interval(200, 300),
            Interval(400, 500),
        ]
    }
    threads = 2

    # Run the function
    regions = divide_chrom_by_span(bed_trees, threads)

    # Calculate expected chunk size
    chrom_start = 0  # min starts: 0
    chrom_end = 500  # max ends: 500
    total_span = chrom_end - chrom_start  # 500
    chunk_size = (total_span + threads - 1) // threads  # (500 + 1) // 2 = 250

    # Expected regions
    expected = [
        f"chr1:{chrom_start}:{chrom_start + chunk_size}",  # chr1:0:250
        f"chr1:{chrom_start + chunk_size}:{chrom_end}",    # chr1:250:500
    ]

    assert regions == expected


def test_divide_chrom_by_span_multiple_chroms():
    bed_trees = {
        "chr1": [Interval(0, 100)],
        "chr2": [Interval(50, 200)],
    }
    threads = 1

    regions = divide_chrom_by_span(bed_trees, threads)

    # When threads=1, should return one region per chrom covering full span
    expected = [
        "chr1:0:100",
        "chr2:50:200",
    ]

    assert regions == expected


def test_divide_chrom_by_span_small_intervals():
    bed_trees = {
        "chr1": [Interval(0, 5)],
    }
    threads = 10  # more threads than span

    regions = divide_chrom_by_span(bed_trees, threads)

    # Even if chunk_size < 1, function should still return valid regions
    # Here chunk_size = (5 + 10 -1)//10 = 1
    expected = [
        "chr1:0:1",
        "chr1:1:2",
        "chr1:2:3",
        "chr1:3:4",
        "chr1:4:5",
    ]

    assert regions == expected
