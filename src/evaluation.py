"""Model fitting / scoring helper shared across the model comparison cells."""
from sklearn.model_selection import cross_val_score
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                              fbeta_score, matthews_corrcoef, roc_auc_score)


def fit_and_score(name, model, X_train, X_test, y_train, y_test, full_X, full_y, cv=5):
    """Fit one model, return (metrics_dict, fitted_model, test_predictions).

    metrics_dict covers accuracy/precision/recall/F1/F2/MCC/ROC-AUC on the
    held-out test set, plus a `cv`-fold cross-validated F1 over the full
    dataset so a single lucky/unlucky split doesn't drive the headline
    numbers.

    F2 (beta=2, recall weighted twice as heavily as precision) is included
    alongside F1 because the error-analysis discussion argues a missed
    phishing site (false negative) is worse than a false alarm for this
    specific threat model - F2 is the metric that actually reflects that
    stated priority, rather than just asserting it in prose.
    """
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]
    cv_f1 = cross_val_score(model, full_X, full_y, cv=cv, scoring="f1")

    metrics = {
        "model": name,
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred),
        "recall": recall_score(y_test, pred),
        "f1": f1_score(y_test, pred),
        "f2": fbeta_score(y_test, pred, beta=2),
        "mcc": matthews_corrcoef(y_test, pred),
        "roc_auc": roc_auc_score(y_test, proba),
        "cv_f1_mean": cv_f1.mean(),
        "cv_f1_std": cv_f1.std(),
    }
    return metrics, model, pred
