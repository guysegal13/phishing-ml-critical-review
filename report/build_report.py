"""
Generates report/Final_Report.pdf from plain text + the figures already
sitting in ../figures. One-off build script, not graded itself.
"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                 ListFlowable, ListItem, PageBreak, Table, TableStyle, KeepTogether)
from reportlab.lib import colors

FIG = os.path.join("..", "figures")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle("TitleBig", parent=styles["Title"], fontSize=20, spaceAfter=4))
styles.add(ParagraphStyle("Sub", parent=styles["Normal"], fontSize=11, textColor=colors.grey, alignment=TA_CENTER, spaceAfter=20))
styles.add(ParagraphStyle("H1", parent=styles["Heading1"], fontSize=15, spaceBefore=18, spaceAfter=8))
styles.add(ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12.5, spaceBefore=12, spaceAfter=6))
styles.add(ParagraphStyle("Body", parent=styles["BodyText"], fontSize=10.3, leading=14.5, spaceAfter=8))
styles.add(ParagraphStyle("BodySmall", parent=styles["BodyText"], fontSize=9.3, leading=12.5, textColor=colors.grey))
styles.add(ParagraphStyle("Caption", parent=styles["BodyText"], fontSize=8.8, leading=11, textColor=colors.grey, alignment=TA_CENTER, spaceAfter=14))

story = []

def h1(text):
    story.append(Paragraph(text, styles["H1"]))

def h2(text):
    story.append(Paragraph(text, styles["H2"]))

def p(text):
    story.append(Paragraph(text, styles["Body"]))

def bullets(items):
    story.append(ListFlowable([ListItem(Paragraph(i, styles["Body"])) for i in items],
                               bulletType="bullet", leftIndent=16, spaceBefore=2, spaceAfter=8))

def fig(name, caption, width=5.6):
    story.append(Spacer(1, 6))
    story.append(Image(os.path.join(FIG, name), width=width * inch, height=width * inch * 0.72))
    story.append(Paragraph(caption, styles["Caption"]))

def table(data, col_widths=None):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8.7),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

# ===========================================================================
# Title
story.append(Spacer(1, 60))
story.append(Paragraph("Detecting Phishing Websites with Machine Learning:", styles["TitleBig"]))
story.append(Paragraph("a reproduction and critique", styles["TitleBig"]))
story.append(Paragraph("Final Project &ndash; Data Science in Cyber (Dr. Uri Itai)", styles["Sub"]))
story.append(Paragraph("Guy Segal &middot; June 2026", styles["Sub"]))
story.append(Spacer(1, 30))
p("""Source critiqued: <i>"Detecting Phishing Websites using Machine Learning"</i> by Sayak Paul,
published under Intel Software Innovators on Medium
(<font color="blue">medium.com/intel-software-innovators/detecting-phishing-websites-using-machine-learning-de723bf2f946</font>),
with the companion GitHub repo
<font color="blue">github.com/sayakpaul/Phishing-Websites-Detection</font>.""")
story.append(PageBreak())

# ===========================================================================
h1("1. Summary of the Source")

p("""The article picks a pretty well-defined problem: given a website, decide whether it's
phishing or legitimate, using a fixed table of pre-computed features rather than the raw page
itself. That's a sensible framing for a tutorial &ndash; it sidesteps the (much harder) problem of
scraping live pages and extracting features in real time, and just focuses on "given these
30 numbers, what's the label." The author is upfront that phishing is a real and costly problem
(stolen credentials, financial fraud, etc.) and that catching it automatically, rather than
relying purely on blacklists, is the motivation.""")

p("""Why it matters: blacklists are reactive by nature, a site has to be reported and verified
before it lands on the list, and by then plenty of victims have already clicked through. A model
trained on structural features of a URL/page can in theory catch a brand-new phishing site on day
one, which is the whole appeal of the machine-learning angle here.""")

h2("Dataset")
p("""The <b>UCI Phishing Websites dataset</b> &ndash; 11,055 rows, 30 features, all pre-encoded as
small categorical integers (mostly -1/1, a few -1/0/1), target column <tt>Result</tt> (-1 =
phishing, 1 = legitimate). Features fall into a few natural groups: things you can read straight
off the URL (IP address used instead of a domain, URL length, presence of "@", use of a shortener,
prefix/suffix tricks like "paypal-secure.com"), things that need a DNS/WHOIS lookup (domain age,
registration length, DNS record), and things that need the actual page content (favicon source,
form action / SFH, anchor tag destinations, iframes). It's a well-known dataset, originally
published alongside a 2014 paper by Mohammad, Thabtah and McCluskey that explains how each feature
was engineered, which is more documentation than most Kaggle datasets get.""")

h2("Proposed solution / methodology")
p("""The author trains three models in increasing order of sophistication: a logistic regression
baseline, a small Keras neural network, and finally a model built with <b>fastai</b> using entity
embeddings for the categorical features, a 1cycle learning rate schedule, and discriminative
learning rates. The -1 labels are remapped to 0 "to stabilize optimization." No feature scaling is
applied (values are already small and bounded) and, notably, the author explicitly decides
<i>against</i> doing any feature selection, reasoning that all 30 features contribute collectively.
An 80/20 train/test split is used, with shuffling.""")

table([
    ["Model", "Reported accuracy"],
    ["Logistic Regression (baseline)", "93.71%"],
    ["Neural network (Keras, Adam optimizer)", "96.52%"],
    ["Fastai model w/ entity embeddings + 1cycle policy", "97.02%"],
], col_widths=[3.6 * inch, 2.0 * inch])

p("""The author's headline claim is that the final fastai model "matches state-of-the-art" results
reported elsewhere in the literature for this same dataset, and that the gain over the plain
neural net comes from the entity embeddings doing a better job representing the categorical
features than one-hot/ordinal encoding would.""")

# ===========================================================================
h1("2. Critical Evaluation")

p("""This is the section where I think the article runs into trouble, and it's worth saying up
front: my issue isn't with the code or the explanations, which are clear and the repo runs fine.
It's with two specific claims, and with a methodological detail the author (like most tutorials
using this dataset, mine included on the first pass) never checks.""")

h2("Claim 1: the entity-embedding model earns its complexity")
p("""The author frames the fastai model's 97.02% as the payoff for a noticeably more involved
pipeline &ndash; entity embeddings for categorical variables, a 1cycle learning rate schedule,
discriminative learning rates layer-by-layer. Embeddings are a genuinely good idea for
<i>high-cardinality</i> categorical features (think zip codes, product IDs, thousands of
categories) where one-hot encoding would blow up the dimensionality and a dense vector
representation lets the model learn useful structure. But every feature in this dataset has only
2 or 3 levels. There's just not much "structure" for an embedding to discover in a 3-category
variable that a one-hot encoding wouldn't already capture directly. In my own reproduction
(section 5 below), a default <b>Random Forest with zero tuning</b> hits 97.7% accuracy on the
same split methodology the author used, and 96.5% once I fix the data leakage issue described
below &ndash; either way, in the same ballpark as the entity-embedding model, for a fraction of
the engineering effort and no GPU. I don't think the article's data supports the implicit claim
that embeddings are the right tool for this particular dataset; it supports "you can also get to
~97% with a much fancier model," which is a different and weaker claim.""")

h2("Claim 2: \"no feature selection needed because every feature contributes\"")
p("""This one is asserted rather than tested in the article &ndash; there's no ablation, no
feature-importance plot, nothing showing that removing a feature actually hurts performance. My
own correlation analysis (notebook section 2) and mutual-information analysis (notebook section 3)
tell a pretty different story: two features, <tt>SSLfinal_State</tt> and <tt>URL_of_Anchor</tt>,
carry the vast majority of the signal (Spearman correlation with the target of -0.74 and -0.70
respectively, far ahead of anything else). On top of that, most of the other 28 features sit in a
heavily skewed 85-90% majority-class band (two, <tt>RightClick</tt> and <tt>Iframe</tt>, go past
90%), which puts a hard ceiling on how much they can possibly contribute &ndash; a feature can't
separate two classes well if 85-95% of rows take the same value regardless of label. That doesn't
mean feature selection would necessarily <i>improve</i> accuracy &ndash; tree models in particular
are pretty good at ignoring useless features on their own &ndash; but "every feature contributes"
as stated isn't backed by anything in the article, and a quick look at the data suggests it's at
best an oversimplification.""")

h2("The methodology problem the article doesn't check: duplicate rows")
p("""This is the part I'd flag as the most serious issue, and it applies to basically every
tutorial built on this dataset, not just this one. <b>47% of the 11,055 rows are exact
duplicates</b> of another row (identical features <i>and</i> identical label), and <b>71% of
rows share their feature vector with at least one other row</b>. Once you do a random 80/20 split
without deduplicating first, a big chunk of the test set ends up being rows the model has
effectively already memorized: in my reproduction, <b>64.6% of the test rows have an exact
feature-vector match already sitting in the training set</b>. That inflates every reported
accuracy number to some degree, including the author's, including mine on the first pass. I
re-ran the comparison after deduplicating (down to 5,785 unique rows) and Random Forest dropped
from 97.7% to 96.5% &ndash; not catastrophic, but not nothing either, and it's exactly the kind of
gap that should be checked and disclosed before calling a number "state of the art."""
)

h2("Is the evaluation methodology appropriate?")
p("""Mostly yes for what it's trying to show (a single train/test split is fine for a tutorial,
nobody's claiming production-grade rigor), but it's missing two things I'd consider standard
practice: cross-validation to get a sense of variance across splits, and a check for duplicate
rows before splitting. I added both in my reproduction. The metrics chosen (accuracy + a
classification report + confusion matrix) are reasonable but a bit thin for a security context;
there's no discussion anywhere of the precision/recall trade-off or what a false negative costs
versus a false positive, which feels like a missed opportunity given the domain.""")

h2("Are the conclusions justified?")
p("""Partially. "You can get phishing detection above 90% accuracy with this dataset and these
methods" is well supported. "The entity-embedding model represents a meaningful improvement and
matches the state of the art" is the part I'd push back on &ndash; my reproduction suggests a much
simpler model gets you almost all the way there, and the comparison wasn't done on a leak-free
split to begin with. I'd call this an example of a generally solid tutorial overselling its most
sophisticated step.""")

# ===========================================================================
h1("3. Feature Engineering Analysis")

p("""Short answer on whether feature engineering happened: not really, on the author's side. The
dataset arrives pre-engineered (the heavy lifting, deciding which 30 properties of a URL/page are
worth computing in the first place, was done by Mohammad et al. back in 2014, not by the article's
author). The article's only real preprocessing step is remapping -1 labels to 0. I went further in
my own notebook and actually tried a few things, with mixed results.""")

h2("Encoding")
p("""The raw -1/0/1 integers implicitly treat the middle category as a number sitting between the
other two, which is a real assumption for the eight 3-level columns (<tt>SSLfinal_State</tt>,
<tt>URL_of_Anchor</tt>, <tt>having_Sub_Domain</tt>, etc.). I tried one-hot encoding those eight
columns instead (30 features become 46) and re-ran logistic regression and Random Forest. Logistic
regression improved a bit (92.8% &rarr; 93.9% accuracy, F1 0.917 &rarr; 0.930), which makes sense:
a linear model benefits from not having to fit a single coefficient across three categories that
might not actually be linearly ordered. Random Forest barely changed (97.7% &rarr; 97.2%, if
anything very slightly worse, basically noise) &ndash; trees split on thresholds regardless of
encoding, so there's nothing to gain there. This is a clean, evidence-backed example of "the right
preprocessing choice depends on the downstream model," not something I'd have known without
testing it.""")

fig("feature_skew.png", "Figure A. Every feature's distribution, ranked by the share of rows taken up by its most common value. Only RightClick (95.7%) and Iframe (90.8%) cross the 90% \"near-constant\" line, but roughly two thirds of the 30 features sit in the heavily-skewed 85-90% band. The handful pulled toward the balanced end (SSLfinal_State, URL_of_Anchor, having_Sub_Domain, web_traffic) are exactly the features that turn out to carry real signal in section 5.", width=4.6)

h2("Scaling")
p("""Not needed and I didn't apply it. Every feature is already bounded to [-1, 1]; I checked
anyway (standardizing before logistic regression) and the accuracy moved by less than 0.1
percentage points. Would matter a lot more if any feature were a raw count instead of a pre-binned
category.""")

h2("Feature creation")
p("""I built a <tt>risk_flag_count</tt> feature: the number of nine "classic" suspicious-URL flags
tripped at once (IP-in-URL, shortener, @ symbol, double-slash redirect, prefix-suffix dash,
abnormal URL, mouseover tricks, pop-ups, iframes), on the security intuition that several weak
signals together should be more convincing than one. It correlates with the target at only 0.10
Spearman, and adding it to Random Forest moved the F1 score from 0.9738 to 0.9718 &ndash;
essentially no effect, within noise. The honest read: the individual flags I picked are each
fairly weak on their own (none were in the top-10 by correlation or mutual information), so
summing weak signals didn't manufacture a strong one. It's a useful negative result &ndash; a
reasonable-sounding feature idea that the data just didn't support.""")

h2("Feature selection")
p("""Mutual information and Spearman correlation rank the features almost identically: a strong
top tier (<tt>SSLfinal_State</tt>, <tt>URL_of_Anchor</tt>), a moderate second tier
(<tt>Prefix_Suffix</tt>, <tt>web_traffic</tt>, <tt>having_Sub_Domain</tt>), and a long tail of
features each contributing very little in isolation. I also found three pairs of features with
|Spearman| above 0.8 between themselves &ndash; <tt>Shortining_Service</tt> &amp;
<tt>double_slash_redirecting</tt> (0.84), <tt>Favicon</tt> &amp; <tt>port</tt> (0.80), and
<tt>Favicon</tt> &amp; <tt>popUpWidnow</tt> (0.94, which has no obvious causal story and is
probably an artifact of how the original dataset was assembled). Dropping the weaker half of each
pair and re-running Random Forest changed the result by less than 0.3 points &ndash; consistent
with the redundancy being real but mostly harmless for a tree-based model.""")

h2("Dimensionality reduction")
p("""I ran a 2-component PCA purely as a visualization, not as model input (with only 30 already
low-dimensional features there's no real need to reduce anything). The two classes separate
reasonably along PC1, but PCA assumes roughly linear/continuous structure which these categorical
features don't really have, so I'd treat this plot as a rough sanity check rather than a real
analytical tool here.""")

h2("Is there redundancy, and how would I tackle it?")
p("""Yes, in two senses: the three highly-correlated feature pairs above, and the dataset-level
redundancy of 71% of rows sharing a feature vector with another row. I'd spot the first kind with
a pairwise correlation scan (what I did) and the second kind with <tt>.duplicated()</tt> on the
feature columns before doing anything else with the data. Tackling it: drop one feature from each
correlated pair (cheap, low risk given trees barely notice), and deduplicate rows before any
train/test split, full stop &ndash; that one isn't really optional once you know it's there.""")

h2("Was the feature engineering meaningful?")
p("""The original 30 features themselves are genuinely well thought out &ndash; each one maps to
a real attacker behavior (registering short-lived domains, hiding the real link behind anchor
text, abusing favicon/iframe loading to mimic a legitimate brand) and there's solid mathematical
intuition behind most of them (e.g. <tt>SSLfinal_State</tt> works because a valid, long-lived
HTTPS certificate from a real CA used to be expensive/slow enough that phishing operations
couldn't easily fake it &ndash; less true today, see the error analysis). What's less convincing
is the implicit claim that all 30 are pulling their weight equally; two features dominate, and
that's worth knowing before scaling this approach to a new dataset.""")

h2("Additional features that could help")
bullets([
    "A real temporal feature &ndash; certificate issue date / domain creation date as a continuous age in days rather than a binarized flag, which would let a model learn a threshold rather than relying on whatever cutoff the original feature used.",
    "WHOIS registrar reputation (some registrars are disproportionately used for throwaway phishing domains) &ndash; not present here at all.",
    "Visual similarity to known brands (logo/layout similarity scores), which catches the cases where the URL itself looks fine but the page is a near-pixel copy of a real login page &ndash; the kind of thing pure URL/structural features will always miss.",
    "Lexical/NLP features on the URL itself (n-gram entropy, edit distance to popular domain names) to catch typosquatting that the current feature set doesn't directly encode.",
])

# ===========================================================================
h1("4. Reproducibility Analysis")

p("""On the whole, this article reproduces well, better than most ML tutorials I've tried to redo
for past coursework. The dataset is a standard, citable UCI dataset rather than something the
author scraped themselves and never published, which already puts it ahead of a lot of blog-post
tutorials.""")

bullets([
    "<b>Code execution:</b> the GitHub repo's notebooks ran without modification for the data loading and the scikit-learn/Keras parts. The one piece I genuinely could not reproduce was the fastai entity-embedding model &ndash; fastai wasn't something I could get installed cleanly in this environment, and fastai's API has changed enough across versions that an old fastai v1 notebook is not a drop-in run today. I flagged this rather than fake it; my closest honest substitute is the small sklearn MLP in section 4 of the notebook, not a true entity-embedding model.",
    "<b>Files and dependencies:</b> the dataset is openly hosted on the UCI repository and downloads cleanly. Standard packages only (pandas, scikit-learn, matplotlib/seaborn) for everything except the fastai step.",
    "<b>Hidden preprocessing:</b> the only preprocessing the article itself does is the -1 &rarr; 0 label remap, which is stated explicitly, nothing hidden there. What <i>is</i> hidden, in the sense that it's not discussed anywhere in the article or in the original dataset documentation I could find, is the duplicate-row situation described in section 2. That's not something the author did wrong, exactly, it's a property of the dataset they didn't go looking for, but it is a hidden issue that affects how the reported numbers should be read.",
    "<b>Overall reproducibility:</b> good for the baseline and neural-net models, partial for the final fastai model due to tooling drift rather than anything the author did poorly. I'd call this a B+/A- on reproducibility, better than most of what's out there for this kind of project.",
])

# ===========================================================================
h1("5. Experimental Results")

h2("What I ran")
p("""All experiments use the same UCI dataset as the article, random_state=42 everywhere a seed
is accepted, and an 80/20 stratified train/test split unless noted. On top of reproducing the
author's logistic-regression baseline, I trained three models the article doesn't use (Random
Forest, scikit-learn's HistGradientBoostingClassifier as a boosted-tree alternative to XGBoost,
and a small MLP as a fair sklearn stand-in for the Keras network), ran 5-fold cross-validation for
each, and then repeated the whole comparison on a deduplicated version of the dataset to isolate
the leakage effect described in section 2.""")

h2("Modifications introduced")
bullets([
    "Recoded the target as 0/1 (phishing = 1) instead of the original -1/1, purely for readability in plots and metric functions.",
    "Added Random Forest, HistGradientBoosting and an MLP as comparison models not present in the source article.",
    "Added 5-fold cross-validation on top of the single train/test split.",
    "Added a deduplicated-dataset rerun to check for train/test leakage.",
    "Tried one-hot encoding, a hand-built risk-count feature, and redundant-feature removal (all described in section 3).",
])

h2("Results &ndash; raw 80/20 split (matches the article's methodology)")
table([
    ["Model", "Accuracy", "Precision", "Recall", "F1", "MCC", "ROC-AUC"],
    ["Logistic Regression", "0.928", "0.934", "0.900", "0.917", "0.853", "0.978"],
    ["Random Forest", "0.977", "0.980", "0.967", "0.974", "0.953", "0.996"],
    ["HistGradientBoosting", "0.969", "0.971", "0.958", "0.965", "0.937", "0.996"],
    ["MLP (small NN)", "0.976", "0.978", "0.966", "0.972", "0.951", "0.996"],
], col_widths=[1.7 * inch, 0.78 * inch, 0.78 * inch, 0.7 * inch, 0.6 * inch, 0.6 * inch, 0.78 * inch])

fig("model_comparison.png", "Figure 1. Accuracy / F1 / MCC / ROC-AUC across the four models, raw 80/20 split.")

h2("Results &ndash; after removing duplicate rows (honest, leak-free estimate)")
table([
    ["Model", "Accuracy", "F1", "MCC", "ROC-AUC"],
    ["Logistic Regression", "0.934", "0.936", "0.869", "0.983"],
    ["Random Forest", "0.965", "0.965", "0.929", "0.994"],
], col_widths=[1.9 * inch, 0.8 * inch, 0.7 * inch, 0.7 * inch, 0.8 * inch])

p("""Logistic regression is essentially unaffected by deduplication (92.8% &rarr; 93.4%, within
the kind of variation you'd see across random seeds anyway). Random Forest drops about 1.2
accuracy points (97.7% &rarr; 96.5%) once the leaked rows are removed &ndash; a real but moderate
effect, not the kind of result that should change anyone's mind about whether tree ensembles work
well here, but exactly the kind of number that should be reported alongside any "state of the
art" claim on this dataset.""")

fig("confusion_matrix.png", "Figure 2. Confusion matrix for the best model (Random Forest) on the raw split.", width=3.6)

fig("roc_curves.png", "Figure 3. ROC curves for all four models &ndash; they're close enough that ROC-AUC alone barely separates them; F1/MCC are more discriminating here.")

h2("Encoding / feature-engineering experiment results")
table([
    ["Variant", "Model", "Accuracy", "F1"],
    ["raw ordinal encoding", "Logistic Regression", "0.928", "0.917"],
    ["one-hot (8 cols)", "Logistic Regression", "0.939", "0.930"],
    ["raw ordinal encoding", "Random Forest", "0.977", "0.974"],
    ["one-hot (8 cols)", "Random Forest", "0.972", "0.968"],
    ["raw + risk_flag_count", "Random Forest", "0.975", "0.972"],
], col_widths=[2.1 * inch, 1.9 * inch, 0.9 * inch, 0.8 * inch])

h2("Feature importance / correlation")
fig("feature_importance.png", "Figure 4. Random Forest feature importance, top 12 &ndash; dominated by the same two features flagged by the correlation analysis.", width=5.0)
fig("mutual_information.png", "Figure 5. Mutual information with the target, top 12 features.", width=5.0)

h2("Error analysis")
p("""Looking at the Random Forest's mistakes on the raw test split: 19 false positives
(legitimate sites flagged as phishing) and 32 false negatives (phishing sites missed entirely).
The pattern in <i>why</i> each type of mistake happens is pretty clean and lines up with the
feature-importance finding above:""")

bullets([
    "False positives have a mean <tt>SSLfinal_State</tt> of about 0.05, near the \"suspicious/ambiguous\" middle category rather than the \"trusted\" end. These look like legitimate sites with an imperfect or unusual SSL setup tripping the model's strongest feature.",
    "False negatives have a mean <tt>SSLfinal_State</tt> of about 0.75, close to the \"trusted\" end. These are phishing sites that managed to obtain a valid-looking HTTPS certificate &ndash; exactly the scenario that's gotten much easier for attackers since free, automated certificate authorities (Let's Encrypt etc.) became widespread well after this dataset's features were designed in 2014.",
])

p("""Cybersecurity-wise, that second pattern is the one I'd worry about in a real deployment: a
feature that was a strong phishing signal a decade ago (a valid SSL cert meant <i>someone vetted
this domain</i>) has weakened over time as cert issuance got automated and cheap. A model leaning
this heavily on one feature is going to degrade as attacker behavior shifts around that exact
feature, which is a textbook adversarial/concept-drift risk for security ML, and it's also a
direct consequence of this dataset having no temporal information (flagged back in section 1 of
the notebook) &ndash; there's no way to check whether this drift is already visible <i>within</i>
the dataset because we don't know when each row was collected.""")

p("""On the false-positive/false-negative trade-off: this run has more false negatives than false
positives, meaning the model currently leans toward under-flagging rather than over-flagging. For
a phishing detector specifically I'd lean toward tolerating more false positives in exchange for
fewer false negatives &ndash; a flagged legitimate site costs a user a moment of friction; a missed
phishing site can cost real money or credentials. That argues for tuning the classification
threshold down rather than leaving it at the default 0.5, something neither the original article
nor my reproduction actually does, but would be the natural next step before any real deployment.""")

# ===========================================================================
h1("6. Conclusions")

h2("Key findings")
bullets([
    "The author's core pipeline reproduces reasonably well: logistic regression, a neural net, and tree ensembles all land in the low-to-high 90s on this dataset, consistent with the article's reported numbers.",
    "47% of the dataset's rows are exact duplicates, and a naive random split leaks ~65% of the test set back into training as memorized rows &ndash; inflating tree-model accuracy by roughly 1.2 points. Nobody using this dataset that I found, including the article, checks for this.",
    "A plain, untuned Random Forest matches the author's much more elaborate fastai entity-embedding model even after fixing that leak (96.5% vs. 97.0%), which undercuts the article's framing of embeddings as the thing that gets you to \"state of the art\" here.",
    "Two features (<tt>SSLfinal_State</tt>, <tt>URL_of_Anchor</tt>) carry most of the predictive signal under three independent measures, contradicting the article's stated assumption that every feature contributes equally.",
    "A hand-built aggregate feature (<tt>risk_flag_count</tt>) that sounded reasonable on paper didn't improve anything &ndash; a useful negative result.",
])

h2("Lessons learned")
p("""The biggest one, by far: check a dataset for duplicate rows <i>before</i> trusting any
train/test split on it, especially when the feature space is small and categorical (low
cardinality means duplicate feature vectors are almost inevitable at this sample size). I went
into this project expecting the interesting part to be comparing models, and it turned out the
data-quality check I almost skipped was the more important finding. Second lesson: a model
beating a fancier model on a leaky split doesn't mean much by itself, it's worth re-checking
under cleaner conditions before drawing conclusions either way, in either direction.""")

h2("Strengths and weaknesses of the proposed solution")
p("""<b>Strengths:</b> the underlying 30-feature set is genuinely well designed, grounded in real
attacker behavior, and documented in an actual academic paper rather than invented ad hoc. The
article's code runs, is reasonably clear, and the overall "structural features + classical ML"
approach is a sound one for this problem.""")
p("""<b>Weaknesses:</b> no check for duplicate/leaked rows before splitting; no feature-importance
or ablation evidence behind the claim that all features contribute; the headline "97% / state of
the art" framing rests on the article's most complex model without comparing it fairly against
simpler baselines; no discussion of the precision/recall trade-off that actually matters for a
security use case; no acknowledgement that the balanced class split doesn't reflect real-world
phishing prevalence.""")

h2("Suggestions for future improvements")
bullets([
    "Deduplicate the dataset (or at least check for leakage) before reporting any accuracy number on it.",
    "Evaluate at multiple decision thresholds, not just the default 0.5, and report precision/recall trade-offs explicitly given how differently false positives and false negatives cost out in a phishing context.",
    "Test whether entity embeddings actually help on a dataset with genuinely high-cardinality categorical features before presenting them as the key driver of an accuracy gain on a low-cardinality one like this.",
    "Add temporal/freshness features (certificate issue date, domain age in days rather than a binarized flag) so a model has a chance of tracking how attacker behavior shifts over time.",
    "Validate against a more realistic class prior (e.g. via a precision-at-low-prevalence calculation) before making any claim about real-world deployment performance.",
])

# ===========================================================================
h1("7. Executive Summary")

p("""This project reproduces and critiques <i>"Detecting Phishing Websites using Machine
Learning"</i> by Sayak Paul, a Medium/Intel Software Innovators article that trains logistic
regression, a neural network, and a fastai model with entity embeddings on the UCI Phishing
Websites dataset (11,055 sites, 30 pre-engineered categorical features), reporting accuracies of
93.71%, 96.52% and 97.02% respectively, with the fastai model's entity embeddings framed as the
key driver of the final improvement.""")

p("""I reproduced the baseline and neural-net results reasonably closely, but couldn't run the
fastai model itself due to tooling/version issues, a genuine reproducibility gap rather than a
finding against the article. More importantly, I found two things the article doesn't mention:
(1) <b>47% of the dataset's rows are exact duplicates</b>, and a random train/test split leaks
~65% of the test set back into training as memorized rows, inflating accuracy by roughly 1.2
points for tree-based models once corrected; and (2) a plain, untuned <b>Random Forest matches or
beats the fastai entity-embedding model</b> even after fixing that leak (96.5% vs. 97.0%), which
undercuts the article's framing of entity embeddings as the thing that gets you to "state of the
art" on this particular dataset.""")

p("""On feature engineering: the 30 features themselves are well designed and grounded in real
attacker behavior, but two of them (<tt>SSLfinal_State</tt>, <tt>URL_of_Anchor</tt>) account for
the large majority of the predictive signal under three independent measures (Spearman
correlation, mutual information, and Random Forest importance), which conflicts with the
article's stated decision to skip feature selection on the assumption that "every feature
contributes." A hand-built aggregate "risk flag count" feature I tried did not improve results,
a useful negative result. Error analysis shows the model's mistakes cluster around ambiguous or
unexpectedly-valid SSL states, including phishing sites that obtained legitimate-looking
certificates, a known weak spot for any detector leaning heavily on certificate validity.""")

p("""<b>Recommendation:</b> I'd recommend this article and dataset as a solid teaching example for
phishing detection with classical ML, but with the caveat that the duplicate-row issue must be
checked and corrected before trusting any reported accuracy number, and that the marginal value
of the entity-embedding step over a simple Random Forest is, on this evidence, smaller than the
article implies.""")

# ===========================================================================
h1("8. Summing It Up")

p("""<b>Problem:</b> binary classification of websites as phishing or legitimate from 30
pre-computed structural/host-based features.""")
p("""<b>Source:</b> "Detecting Phishing Websites using Machine Learning" by Sayak Paul (Medium /
Intel Software Innovators), GitHub repo <tt>sayakpaul/Phishing-Websites-Detection</tt>.""")
p("""<b>Dataset:</b> UCI Phishing Websites dataset, 11,055 rows, 30 categorical features, target
<tt>Result</tt>.""")
p("""<b>Methodology:</b> reproduced the author's logistic-regression baseline; added Random
Forest, HistGradientBoosting and an MLP for comparison; ran the comparison again after
deduplicating rows; tried one-hot encoding, a custom aggregate feature, and redundant-feature
removal; used Spearman/Kendall correlation and mutual information (justified over Pearson given
the categorical, non-continuous nature of every feature) to identify which features actually drive
the predictions; analyzed false positives and false negatives for the best model.""")
p("""<b>Main findings of the reproduction:</b> baseline numbers reproduce reasonably closely; the
dataset has a serious duplicate-row problem (47% exact duplicates) that inflates naive accuracy
estimates by roughly 1.2 points for tree models; a simple Random Forest matches the author's most
complex model once that's corrected for; two features dominate the prediction far more than the
article's "no feature selection needed" framing suggests.""")
p("""<b>Were the author's claims supported?</b> Partly. The core claim that ML can detect
phishing well on this dataset (90%+ accuracy) is well supported. The claim that the
entity-embedding model represents a meaningful, necessary improvement and "matches state of the
art" is not well supported by my reproduction &ndash; a much simpler model gets you almost all the
way there, and the comparison itself wasn't checked for the leakage issue described above.""")
p("""<b>Most important insight:</b> with a dataset this categorical and this small in feature
count, the choice of model matters far less than people might assume, and basic data hygiene
(checking for duplicate rows before splitting) matters more than the choice between a neural net
and a tree ensemble.""")
p("""<b>Would I recommend this approach for similar problems?</b> Yes, with caveats: the
underlying feature set and the general "structural features + classical ML" approach is a
genuinely solid starting point for phishing detection, and I'd reuse it. I would not reuse the
entity-embedding step without first establishing that the categorical features in a new dataset
actually have enough cardinality/structure to benefit from it, and I would always deduplicate rows
before splitting on this specific dataset.""")
p("""<b>Final conclusion:</b> a well-documented, mostly reproducible tutorial built on a
respectable academic dataset, let down a little by an unverified claim about its most
sophisticated model and a data-quality issue that nobody using this dataset (the author, me on my
first pass, and apparently most of the other tutorials I found while researching this project)
seems to have checked for.""")

doc = SimpleDocTemplate("Final_Report.pdf", pagesize=LETTER,
                         leftMargin=0.85 * inch, rightMargin=0.85 * inch,
                         topMargin=0.8 * inch, bottomMargin=0.8 * inch,
                         title="Detecting Phishing Websites with Machine Learning - Final Report")
doc.build(story)
print("report written.")
