import pytest
import numpy as np
from aci.logic.report import calculate_gini

def test_gini_perfect_equality():
    """
    If all amplicons have the same depth, Gini should be 0.
    """
    depths = np.array([100, 100, 100, 100])
    gini = calculate_gini(depths)
    
    # Floating point math might return 0.000000001, so use approx
    assert gini == pytest.approx(0, abs=1e-5)

def test_gini_high_inequality():
    """
    If one amplicon has everything, Gini should be close to 1.
    """
    # 1 amplicon has 100 reads, 4 have 0
    depths = np.array([100, 0, 0, 0, 0])
    gini = calculate_gini(depths)
    
    # In a population of 5, with one holding all wealth:
    # Theoretical max Gini for n=5 is (n-1)/n = 0.8
    assert gini > 0.7

def test_gini_empty_or_zero():
    """
    Handle edge cases gracefully.
    """
    # All zeros
    depths = np.array([0, 0, 0])
    # Depending on implementation, this might be 0 or NaN.
    # Your implementation adds epsilon, so it should be stable near 0.
    assert calculate_gini(depths) < 0.1