# Marketing Mix Modeling with Google Meridian

A portfolio project demonstrating end-to-end **Marketing Mix Modeling (MMM)** using Google's open-source [Meridian](https://github.com/google/meridian) library.  
Built by [Laura Keita](https://github.com/laurakeita) — Growth Marketing & Strategy Operations, HEC Paris MBA.

---

## Project Structure

```
MMM/
├── MMM_meridian.ipynb       # Full analysis notebook (outputs included)
├── data/
│   ├── sample_data.csv          # 10-row preview of the dataset
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

## Workflow

| Section | What it does |
|---------|-------------|
| Data Audit | Detects media/impression/KPI columns dynamically; runs spend-share, correlation, and VIF analysis |
| Model Training | Fits a Bayesian MMM with log-normal ROI priors using Meridian's MCMC sampler (5 chains × 2 000 posterior draws) |
| Model Diagnostics | Checks convergence (trace plots, R-hat ≤ 1.1), plots contribution waterfall, ROI bar chart, response curves, adstock decay |
| Budget Optimisation | Re-allocates the existing budget to maximise revenue; spend constraints are derived dynamically from actual channel spend |
| Attribution Validation | Compares Meridian's estimated ROI against known ground-truth values to quantify model accuracy |

---

## Key Design Decisions

- **Dynamic column detection** — media, impression, and KPI columns are inferred from column names rather than hardcoded, making the pipeline portable across datasets.
- **Dynamic date ranges** — optimization period and summary reports use `data['date'].min()/max()` instead of hardcoded strings.
- **VIF excludes the time index** — the synthetic `t` column is dropped before VIF calculation to avoid spurious multicollinearity.
- **Controls guarded** — `Offline Discount` is only passed to Meridian if the column exists in the loaded data.

---

## Quick Start (Google Colab)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/laurakeita/MMM/blob/main/MMM_meridian.ipynb)

```python
# 1. Install dependencies
!pip install git+https://github.com/google/meridian.git altair -q

# 2. Mount Drive and upload your CSV
from google.colab import drive
drive.mount('/content/drive')

# 3. Run all cells top to bottom
```

---

## Results

**Model fit** — R²: 0.30 · MAPE: 9%

> R² reflects the complexity of modelling weekly revenue with limited spend variation in synthetic data — MAPE of 9% confirms the model tracks directional patterns well.

**Channel ROI** (posterior mean, Jan 2023 – Dec 2024):

| Channel | ROI | Contribution |
|---------|-----|-------------|
| Meta | 1.83 | 13.0% |
| Google | 1.94 | 12.9% |
| TikTok | 2.00 | 5.9% |
| Baseline | — | 68.1% |

**Budget optimisation** (fixed budget, ±30% constraint):
- Google: 40% → 44% (+$65k)
- Meta: 43% → 38% (−$61k)
- TikTok: 18% → 17% (−$4k)
- Incremental revenue lift: ~+$6k

---

## Tech Stack

`Python` · `Google Meridian` · `TensorFlow Probability` · `ArviZ` · `pandas` · `seaborn` · `statsmodels` · `altair`
