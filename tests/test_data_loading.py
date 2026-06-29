import os
import pandas as pd

from src.data_loading import load_phishing_arff

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "phishing_websites.arff")


def test_shape_and_dtypes():
    df = load_phishing_arff(DATA_PATH)
    assert df.shape == (11055, 31)
    assert (df.dtypes == "int64").all()


def test_no_missing_values():
    df = load_phishing_arff(DATA_PATH)
    assert df.isna().sum().sum() == 0


def test_target_column_present_with_expected_labels():
    df = load_phishing_arff(DATA_PATH)
    assert "Result" in df.columns
    assert set(df["Result"].unique()) == {-1, 1}


def test_feature_values_are_small_categories():
    df = load_phishing_arff(DATA_PATH)
    features = df.drop(columns=["Result"])
    # every feature in this dataset is documented as -1/0/1 valued
    assert features.apply(lambda s: s.isin([-1, 0, 1]).all()).all()
