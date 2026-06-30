# Assignment requirement checklist

Self-audit against the "Final Project - Data Science in Cyber" spec (Dr. Uri Itai). Kept in the
repo so it's easy to re-check before submission and to have on hand if asked to walk through the
project verbally. Every line below points at an exact location: PDF page number, notebook cell
index (open the notebook and use Cell > ... or just count from the top, cell 0 is the title cell),
or file path.

## Source selection

| Requirement | Status | Where |
|---|---|---|
| Topic from the approved list | done | Phishing Detection |
| Source clearly defines a problem | done | report p.2 (Summary of the Source) |
| Source proposes a solution | done | report p.2 |
| Source includes an implementation or GitHub repo | done | README "Source material"; `sayakpaul/Phishing-Websites-Detection` |
| Source provides data or enough info to reproduce | done | UCI Phishing Websites dataset, public, `data/phishing_websites.arff` |

## PDF Report (`report/Final_Report.pdf`, 14 pages)

**1. Summary of the Source** - report p.2
- [x] problem addressed
- [x] why it's important
- [x] proposed solution
- [x] dataset used
- [x] model / methodology employed

**2. Critical Evaluation** - report p.3-4
- [x] main claims made by the author ("Claim 1", "Claim 2" subsections)
- [x] whether claims are supported by evidence (entity-embedding claim challenged with my own RF numbers)
- [x] whether evaluation methodology is appropriate (own subsection, p.4)
- [x] weaknesses / limitations (duplicate-row leakage finding)
- [x] whether conclusions are justified (own subsection, p.4)
- [x] explicit explanation where my findings contradict the author's (the embeddings-aren't-earning-their-complexity argument)

**3. Feature Engineering Analysis** - report p.4-6
- [x] whether feature engineering was performed (p.4, "not really on the author's side")
- [x] which features were used
- [x] transformations explained with why/effect/evidence: encoding (p.4-5, accuracy before/after), scaling (p.6), creation (p.6, risk_flag_count with correlation + before/after F1), selection (p.6, MI + correlation), dimensionality reduction (p.6, PCA)
- [x] redundancy: is there any, how to spot it, how to tackle it (p.6, three correlated pairs + fix)
- [x] meaningful FE: math intuition + cybersecurity angle (p.6, SSLfinal_State CA-cost discussion)
- [x] additional features that could help (p.6, bulleted list: WHOIS reputation, visual similarity, lexical/NLP features, real temporal age)

**4. Reproducibility Analysis** - report p.6-7
- [x] does the code execute successfully
- [x] are required files/dependencies available
- [x] hidden preprocessing steps (duplicate-row issue flagged as the "hidden" one)
- [x] overall reproducibility verdict

**5. Experimental Results** - report p.7-11
- [x] experiments performed ("What I ran")
- [x] modifications introduced (explicit bullet list)
- [x] models trained (4: LR, RF, HistGradientBoosting, MLP)
- [x] evaluation metrics (accuracy/precision/recall/F1/F2/MCC/ROC-AUC table)
- [x] obtained results (raw-split table + dedup table + encoding-experiment table)
- [x] error analysis subsection (FP/FN patterns, SSLfinal_State pattern) - belongs here per the notebook's own section numbering, not as a standalone report section

**6. Conclusions** - report p.12
- [x] key findings (bulleted)
- [x] lessons learned
- [x] strengths and weaknesses of the proposed solution
- [x] suggestions for future improvements

**7. Executive Summary** - report p.13, ~1 page
- [x] present

**8. Summing It Up** - report p.14
- [x] problem addressed
- [x] selected article/blog/tutorial
- [x] dataset used
- [x] methodology employed
- [x] main findings of the reproduction
- [x] whether author's claims were supported
- [x] most important insights
- [x] recommendation for similar problems
- [x] final conclusion

## Python Notebook (`notebook/phishing_detection_critical_review.ipynb`, 75 cells, executes clean, 0 errors)

**1. Data Loading** - cells 1-14
- [x] data loading (cell 3)
- [x] data inspection (cell 4)
- [x] data size, feature types (cell 5)
- [x] temporal analysis (cell 7 - none exist, explicitly flagged as a limitation)
- [x] missing value analysis (cell 8)
- [x] column / index names sense check (cells 10-11 - catches the `registeration` typo)
- [x] handling single-value / irrelevant features (cell 12 - none found)
- [x] duplicated features (cell 13 - duplicated **rows** found and quantified, no duplicated **columns**)

**2. Exploratory Data Analysis** - cells 15-37
- [x] feature distributions (cell 19, the sorted skew chart)
- [x] missing values analysis (cell 8, cross-referenced)
- [x] outlier analysis (cells 21-23 - reframed as rare-category analysis since features are categorical)
- [x] temporal features analysis (cell 7 - N/A, explained why)
- [x] crosstab / group-by analysis (cells 25, 27)
- [x] correlation analysis with justified methodology (cells 29-34: Pearson ruled out, Spearman + Kendall + Cramer's V all computed and cross-checked, with math/assumptions/advantages discussed in markdown)
- [x] class imbalance / prevalence (cell 17 - real-world meaning, sampling bias, "did the author address this" all discussed)
- [x] relevant visualizations (9 saved figures: class balance, feature skew, correlation heatmap, MI, PCA, model comparison, confusion matrix, ROC curves, feature importance)

**3. Feature Engineering** - cells 38-52
- [x] encoding categorical variables, which method and why (cells 39-40, one-hot vs ordinal with before/after numbers)
- [x] feature scaling (cell 41 - tested, found unnecessary, explained why)
- [x] feature creation (cells 42-44 - `risk_flag_count`)
- [x] feature selection (cells 45-49 - mutual information + redundancy-based drop)
- [x] dimensionality reduction when appropriate (cells 50-52 - PCA, with an honest caveat about its fit for categorical data)

**4. Model Training** - cells 53-63
- [x] at least 2 models trained (4: Logistic Regression, Random Forest, HistGradientBoosting, MLP)
- [x] fixed random seed (`RANDOM_STATE = 42`, used everywhere a seed is accepted)
- [x] train/test split (80/20 stratified) **and** cross-validation (5-fold)

**5. Evaluation** - cells 64-69
- [x] appropriate classification metrics (accuracy, precision, recall, F1, F2, MCC, ROC-AUC, confusion matrix)
- [x] each metric given both a mathematical definition and a cybersecurity interpretation (cell 65)
- [x] FP/FN implications discussed per metric (cell 65)
- [x] justification for metrics included/excluded (cell 65 explains why F-beta stops at F2, why MAE/RMSE/R2 don't apply)

**6. Error Analysis** - cells 70-73
- [x] examples of model failures (FP/FN counts and a concrete feature pattern)
- [x] patterns in the errors (SSLfinal_State split between FP and FN)
- [x] cybersecurity implications (cert-issuance-got-cheap argument)
- [x] FP/FN trade-off discussed

## Code Quality Requirements

- [x] short, focused functions - `src/data_loading.py`, `src/feature_engineering.py`, `src/evaluation.py`, every function under ~25 lines
- [x] meaningful variable names
- [x] no unnecessary loops - the only loops are a genuinely-needed pairwise comparison (`find_redundant_pairs`) and the model-training loop (avoids 4x copy-pasted training code)
- [x] proper use of pandas / numpy / scikit-learn
- [x] clear separation between preprocessing, EDA, training, evaluation - both within the notebook's section structure and via the `src/` module boundary
- [x] accurate, informative comments in English
- [x] avoid duplicated code - reusable logic lives once in `src/` and is imported by the notebook (verified: `cramers_v`, `risk_flag_count`, `find_redundant_pairs`, `fit_and_score`, `load_phishing_arff` each have exactly one implementation)
- [x] fixed random seeds when appropriate
- [x] train/test split or cross-validation - both used

## Submission Requirements

- [x] public GitHub repository - https://github.com/guysegal13/phishing-ml-critical-review
- [x] PDF report - `report/Final_Report.pdf`
- [x] Python notebook - `notebook/phishing_detection_critical_review.ipynb`
- [x] supporting code files - `src/`, `tests/`, `report/build_report.py`
- [x] README containing:
  - [x] project description
  - [x] link to the selected article/blog/tutorial
  - [x] link to the original GitHub repo
  - [x] execution instructions
  - [x] dataset source

## Known, explicitly-disclosed gap (not hidden)

- The author's final model uses `fastai` with entity embeddings. `fastai` could not be installed
  cleanly in this environment and its API has drifted enough that an old v1 notebook isn't a
  drop-in run today. This is disclosed in report section 4 (Reproducibility Analysis, p.6) rather
  than silently skipped or faked - the closest honest substitute reproduced instead is a plain
  sklearn MLP (notebook section 4).
