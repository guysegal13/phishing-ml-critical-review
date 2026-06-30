import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

from src.evaluation import fit_and_score


def _toy_dataset():
    X, y = make_classification(n_samples=300, n_features=6, n_informative=4,
                                random_state=42)
    X = pd.DataFrame(X, columns=[f"f{i}" for i in range(6)])
    y = pd.Series(y)
    return X, y


def test_fit_and_score_returns_expected_keys():
    X, y = _toy_dataset()
    X_train, X_test = X.iloc[:240], X.iloc[240:]
    y_train, y_test = y.iloc[:240], y.iloc[240:]

    metrics, model, pred = fit_and_score(
        "LogReg", LogisticRegression(), X_train, X_test, y_train, y_test, X, y, cv=3
    )

    expected_keys = {"model", "accuracy", "precision", "recall", "f1", "f2",
                      "mcc", "roc_auc", "cv_f1_mean", "cv_f1_std"}
    assert expected_keys == set(metrics.keys())
    assert len(pred) == len(y_test)


def test_fit_and_score_on_separable_data_is_accurate():
    X, y = _toy_dataset()
    X_train, X_test = X.iloc[:240], X.iloc[240:]
    y_train, y_test = y.iloc[:240], y.iloc[240:]

    metrics, _, _ = fit_and_score(
        "LogReg", LogisticRegression(), X_train, X_test, y_train, y_test, X, y, cv=3
    )
    # this synthetic dataset is comfortably separable, a sane classifier
    # should do well above chance
    assert metrics["accuracy"] > 0.8
