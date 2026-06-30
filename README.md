# Detecting Phishing Websites with Machine Learning - reproduction & critique

Final project for Data Science in Cyber (Dr. Uri Itai). The assignment was to pick a
published article/blog/tutorial in a cybersecurity + ML topic, reproduce it, and critically
check whether the author's claims actually hold up.

I picked phishing website detection. what's in here: the source article trains
logistic regression -> a neural net -> a fastai model with entity embeddings on the classic UCI
Phishing Websites dataset, topping out at ~97% accuracy and calling that "state of the art." I
reproduced the pipeline, added a couple of models the author didn't try (mainly Random Forest),
and along the way found that ~47% of the dataset's rows are exact duplicates, which leaks into a
naive train/test split and inflates the numbers a bit. Full writeup is in the PDF report.

## What's here

```
notebook/   phishing_detection_critical_review.ipynb - the actual analysis: data loading,
            EDA, feature engineering experiments, model training (4 models), evaluation,
            error analysis. Fully executed, all outputs/plots saved in the notebook.
report/     Final_Report.pdf - the written report (summary, critical evaluation, feature
            engineering analysis, reproducibility analysis, experimental results,
            conclusions, executive summary, summing up).
            build_report.py - script that regenerates the PDF from the figures in plots/.
src/        small reusable module the notebook imports from instead of redefining things
            inline: data_loading.py (arff parser), feature_engineering.py (Cramer's V,
            redundancy check, risk-flag count, majority-class share), evaluation.py
            (the fit/score helper used for every model in the comparison).
tests/      pytest unit tests for everything in src/.
data/       phishing_websites.arff - the raw dataset, as downloaded.
plots/      charts produced by the notebook, saved as PNGs (also embedded in the PDF).
```

## Source material

- Article: ["Detecting Phishing Websites using Machine Learning"](https://medium.com/intel-software-innovators/detecting-phishing-websites-using-machine-learning-de723bf2f946) by Sayak Paul (Intel Software Innovators, Medium).
- Original GitHub repo: [sayakpaul/Phishing-Websites-Detection](https://github.com/sayakpaul/Phishing-Websites-Detection)

## Dataset

[UCI Machine Learning Repository - Phishing Websites Data Set](https://archive.ics.uci.edu/dataset/327/phishing+websites)
(11,055 rows, 30 pre-engineered categorical features, target `Result`). Downloaded directly from
`archive.ics.uci.edu` and included in `data/` as-is.

## Running it

```bash
pip install -r requirements.txt
jupyter notebook notebook/phishing_detection_critical_review.ipynb
```

The notebook adds the repo root to `sys.path` and imports from `src/`, and reads
`data/phishing_websites.arff` via a relative `../data/...` path, so just open it from inside
`notebook/` (which is what `jupyter notebook` does by default) and run all cells top to bottom.
It'll regenerate everything in `plots/` along the way. Everything that uses randomness is
seeded (`random_state=42`), so re-running should reproduce the same numbers reported in the PDF.

To rebuild the PDF report after re-running the notebook (e.g. if a figure changed):

```bash
cd report
python build_report.py
```

To run the unit tests for the `src/` helpers:

```bash
pytest tests/
```
