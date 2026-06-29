"""Feature engineering / association helpers used in the EDA and feature
engineering sections of the notebook."""
import numpy as np
import pandas as pd
from scipy.stats import contingency


def cramers_v(x, y):
    """Cramer's V association measure between two categorical series.

    Unlike Pearson/Spearman this makes no assumption about ordering between
    categories, which fits the nominal (not really ordinal) nature of some
    of the 3-level columns in this dataset.
    """
    table = pd.crosstab(x, y)
    chi2 = contingency.chi2_contingency(table)[0]
    n = table.sum().sum()
    r, k = table.shape
    return np.sqrt((chi2 / n) / (min(r, k) - 1))


def risk_flag_count(features, risky_cols, risky_value=-1):
    """Count, per row, how many of `risky_cols` are at the 'risky' value.

    Security intuition: a single suspicious indicator might be a false
    alarm, several at once is a lot more convincing.
    """
    return (features[risky_cols] == risky_value).sum(axis=1)


def find_redundant_pairs(corr_matrix, threshold=0.8):
    """Return (col_a, col_b, correlation) for every feature pair whose
    absolute correlation exceeds `threshold`, based on a pre-computed
    correlation matrix (e.g. features.corr(method='spearman'))."""
    pairs = []
    cols = corr_matrix.columns
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            value = corr_matrix.iloc[i, j]
            if abs(value) > threshold:
                pairs.append((cols[i], cols[j], round(float(value), 3)))
    return pairs


def majority_class_share(features):
    """For each column, the share of rows taken up by its most common
    value. A quick way to spot near-constant / low-information features
    without having to eyeball a distribution plot per column."""
    return features.apply(lambda s: s.value_counts(normalize=True).max())
