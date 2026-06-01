# Incrementality Measurement and Marketing Mix Modeling with Google Meridian

This project evaluates whether Marketing Mix Modeling (MMM) can accurately recover underlying channel-level media effects using Google's [Meridian](https://github.com/google/meridian) framework.  
Built by [Laura Keita](https://github.com/laurakeita) — Growth Marketing & Strategy Operations, HEC Paris MBA.

Rather than focusing solely on prediction accuracy, the project validates attribution performance through synthetic datasets with known ground-truth ROI and contribution values.

The project explores key challenges commonly faced by Measurement Science, Growth Analytics, and Strategy teams:

- **Incrementality Measurement** — can the model isolate incremental revenue driven by each channel?
- **Marketing Attribution** — does attribution accuracy hold when channels move together?
- **Causal Impact Estimation** — how closely do estimated effects match true causal parameters?
- **Budget Allocation Optimization** — how should media budgets be reallocated to maximise incremental business impact?
- **Channel Identifiability** — how does spend correlation between channels affect attribution recovery?
- **Bayesian Marketing Mix Modeling** — MCMC-based posterior estimation with convergence diagnostics

A key finding from this project is that strong predictive performance does not necessarily imply accurate attribution recovery. The results demonstrate how channel identifiability can significantly influence incrementality measurement even when model convergence and predictive accuracy remain strong.

---

## Project Structure

```
MMM/
├── MMM_meridian.ipynb       # Full analysis notebook (outputs included)
├── data/
│   └── synthetic_mmm_data.csv  # 104-week synthetic dataset (Meta, Google, TikTok)
├── outputs/
│   ├── summary_output.html      # Meridian MMM Report — model fit, ROI, response curves
│   └── optimization_output.html # Budget reallocation report (±30% constraints)
├── images/
│   ├── rhat_convergence.png     # R-hat convergence diagnostic (all chains ≤ 1.1)
│   └── roi_by_channel.png       # ROI by channel with 90% credible interval
└── requirements.txt
```

---

## Business Relevance

This project reflects common measurement challenges faced by Growth, Marketing Science, Strategy & Operations, and Resource Management teams.

Key business questions addressed:

- Which channels drive **incremental revenue** rather than simply capture existing demand?
- How accurately can attribution models recover underlying **causal effects**?
- How should marketing budgets be reallocated to maximise **incremental business impact**?
- What are the limitations of measurement frameworks when media channels exhibit strong correlation?
- How can organisations improve **resource allocation decisions** using data-driven incrementality measurement?

These questions are directly relevant to measurement and optimisation functions across technology, e-commerce, and digital platform businesses.

---

## Workflow

| Section | What it does |
|---------|-------------|
| Data Audit | Detects media/impression/KPI columns dynamically; runs spend-share, correlation, and VIF analysis to assess channel identifiability risks |
| Model Training | Fits a Bayesian MMM with log-normal ROI priors using Meridian's MCMC sampler (5 chains × 2 000 posterior draws) |
| Model Diagnostics | Checks convergence (trace plots, R-hat ≤ 1.1), plots contribution waterfall, ROI bar chart, response curves, adstock decay |
| Budget Optimisation | Re-allocates the existing budget to maximise incremental revenue; spend constraints derived dynamically from actual channel spend |
| Attribution Validation | Compares Meridian's estimated ROI against known ground-truth values to quantify attribution accuracy and ROI recovery error |

---

## Validation Framework

The project evaluates MMM performance using two complementary approaches.

### Prediction Validation

| Metric | Purpose |
|--------|---------|
| R² | Proportion of revenue variance explained by the model |
| MAPE | Mean absolute percentage error on predicted revenue |
| wMAPE | Weighted MAPE, accounting for revenue magnitude |

These metrics evaluate how well the model predicts observed revenue.

### Attribution Validation

| Metric | Purpose |
|--------|---------|
| ROI Recovery Error | Gap between estimated and ground-truth channel ROI |
| Contribution Recovery Error | Accuracy of channel contribution share estimates |
| Ground-Truth ROI Comparison | Direct comparison against known synthetic parameters |

These metrics evaluate whether the model can accurately recover underlying media effects — not just fit revenue trends.

> **Key distinction:** Predictive accuracy does not guarantee attribution accuracy. A model can achieve low MAPE while significantly mis-attributing revenue across channels.

---

## Key Design Decisions

- **Dynamic column detection** — media, impression, and KPI columns are inferred from column names rather than hardcoded, making the measurement framework portable across datasets.
- **Dynamic date ranges** — optimisation period and summary reports use `data['date'].min()/max()` instead of hardcoded strings.
- **VIF analysis before modelling** — Variance Inflation Factor is calculated across channels to assess multicollinearity and flag potential channel identifiability issues prior to model fitting.
- **Controls guarded** — `Offline Discount` is only passed to Meridian if the column exists in the loaded data.

---

## Quick Start (Google Colab)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/laurakeita/meridian-mmm-attribution-validation/blob/main/MMM_meridian.ipynb)

```python
# 1. Install dependencies
!pip install git+https://github.com/google/meridian.git altair -q

# 2. Mount Drive and upload your CSV
from google.colab import drive
drive.mount('/content/drive')

# 3. Run all cells top to bottom
```

---

## Key Results

| Metric | Result |
|--------|-------:|
| R-hat | 1.001 |
| R² | 0.30 |
| MAPE | 9% |
| wMAPE | 9% |
| ROI Recovery Error | 24.9% |

### Channel ROI (posterior mean, Jan 2023 – Dec 2024)

| Channel | ROI | Contribution |
|---------|----:|-------------|
| Meta | 1.83 | 13.0% |
| Google | 1.94 | 12.9% |
| TikTok | 2.00 | 5.9% |
| Baseline | — | 68.1% |

### Attribution Validation

| Channel | Ground-Truth ROI | Estimated ROI | Recovery Error |
|---------|----------------:|-------------:|--------------:|
| Meta | 2.07 | 1.80 | 13% |
| Google | 3.00 | 1.90 | 37% |
| **Average** | | | **24.9%** |

Although the model achieved strong convergence and prediction performance, attribution recovery remained more challenging due to channel identifiability limitations — particularly for Google, where limited spend variation makes it harder to isolate incremental effects.

### Budget Optimisation (fixed budget, ±30% constraint)

| Channel | Current | Optimised | Change |
|---------|--------:|----------:|-------:|
| Google | 40% | 44% | +$65k |
| Meta | 43% | 38% | −$61k |
| TikTok | 18% | 17% | −$4k |
| **Incremental lift** | | | **~+$6k** |

---

## Key Learning

A major finding from this project is that **attribution accuracy and prediction accuracy are fundamentally different objectives** in marketing measurement.

Although the model achieved strong convergence (R-hat ≈ 1.001) and low prediction error (MAPE ≈ 9%), channel-level ROI recovery remained imperfect — with an average recovery error of 24.9%.

The results suggest that attribution performance is heavily influenced by **channel identifiability**. When multiple media channels move together, MMM can successfully estimate overall media impact while still struggling to isolate individual channel causal effects. This is a known limitation in Bayesian MMM frameworks and reflects a common real-world challenge faced by growth, measurement, and marketing science teams.

**Key takeaway:** Low prediction error does not imply accurate attribution recovery. Organisations relying solely on MAPE or R² to validate their measurement framework risk making resource allocation decisions based on mis-attributed channel effects.

---

## Tech Stack

`Python` · `Google Meridian` · `Bayesian MMM` · `Incrementality Measurement` · `Attribution Analysis` · `Budget Optimisation` · `Marketing Measurement` · `Causal Impact Estimation` · `TensorFlow Probability` · `ArviZ` · `pandas` · `statsmodels`
