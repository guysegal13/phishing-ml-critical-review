import numpy as np
import pandas as pd

from src.feature_engineering import (cramers_v, risk_flag_count,
                                      find_redundant_pairs, majority_class_share)


def test_cramers_v_is_high_for_perfectly_associated_columns():
    x = pd.Series([0, 0, 1, 1] * 25)
    y = x.copy()  # identical -> perfect association
    # scipy applies Yates' continuity correction by default on 2x2 tables,
    # so this lands just under 1.0 rather than exactly at it
    assert cramers_v(x, y) > 0.95


def test_cramers_v_is_low_for_independent_columns():
    rng = np.random.RandomState(0)
    x = pd.Series(rng.randint(0, 2, size=2000))
    y = pd.Series(rng.randint(0, 2, size=2000))
    assert cramers_v(x, y) < 0.1


def test_risk_flag_count_counts_correctly():
    features = pd.DataFrame({
        "a": [-1, -1, 1, 1],
        "b": [-1, 1, -1, 1],
        "c": [-1, 1, 1, 1],
    })
    counts = risk_flag_count(features, ["a", "b", "c"], risky_value=-1)
    assert list(counts) == [3, 1, 1, 0]


def test_find_redundant_pairs_detects_high_correlation():
    corr = pd.DataFrame(
        [[1.0, 0.95, 0.1], [0.95, 1.0, 0.05], [0.1, 0.05, 1.0]],
        columns=["a", "b", "c"], index=["a", "b", "c"],
    )
    pairs = find_redundant_pairs(corr, threshold=0.8)
    assert pairs == [("a", "b", 0.95)]


def test_find_redundant_pairs_empty_when_below_threshold():
    corr = pd.DataFrame(
        [[1.0, 0.3], [0.3, 1.0]], columns=["a", "b"], index=["a", "b"],
    )
    assert find_redundant_pairs(corr, threshold=0.8) == []


def test_majority_class_share():
    features = pd.DataFrame({
        "a": [1, 1, 1, -1],   # 75% majority
        "b": [1, -1, 1, -1],  # 50% majority (tie -> .max() picks either, both 0.5)
    })
    shares = majority_class_share(features)
    assert shares["a"] == 0.75
    assert shares["b"] == 0.5
