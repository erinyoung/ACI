import pytest
import pandas as pd
import numpy as np
from aci.utils.group_mean import group_mean


def test_group_mean():
    # Create sample data mimicking your input DataFrame structure
    data = {
        "bam": ["sample1", "sample1", "sample1", "sample2", "sample2"],
        "pos": [100, 600, 700, 200, 900],
        "cov": [10, 20, 30, 40, 50],
    }
    df = pd.DataFrame(data)

    # Calculate group means for 'sample1'
    result = group_mean(df, "sample1")

    # Expected groups:
    # Positions 100 -> group 0 (floor(100/500) = 0)
    # Positions 600, 700 -> group 1 (floor(600/500) = 1, fl
