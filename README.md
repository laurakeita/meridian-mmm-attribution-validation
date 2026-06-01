# Marketing Mix Modeling with Google Meridian

A portfolio project demonstrating end-to-end **Marketing Mix Modeling (MMM)** using Google's open-source [Meridian](https://github.com/google/meridian) library.  
Built by [Laura Keita](https://github.com/laurakeita) — Growth Marketing & Strategy Operations, HEC Paris MBA.

---

## Project Structure

```
MMM/
├── data/
│   ├── sample_data.csv          # 10-row preview of the dataset
│   └── synthetic_mmm_data.csv  # 104-week synthetic dataset (Meta, Google, TikTok)
├── notebooks/
│   ├── 01_data_audit.ipynb          # EDA: spend share, correlation, VIF
│   ├── 02_train_meridian_mmm.ipynb  # Bayesian MMM training
│   ├── 03_model_diagnostics.ipynb   # Trace plots, R-hat, media charts
│   ├── 04_budget_optimization.ipynb # ROI-based budget reallocation
│   ├── 05_synthetic_validation.ipynb# Ground-truth recovery validation
│   └── 06_attribution_validation.ipynb # Estimated vs. ground-truth ROI comparison
├── outputs/              # Generated HTML reports (Colab → Drive)
└── images/               # Exported charts
```

---

## Workflow

| Notebook | What it does |
|----------|-------------|
| `01_data_audit` | Detects media/impression/KPI columns dynamically; runs spend-share, correlation, and VIF analysis |
| `02_train_meridian_mmm` | Fits a Bayesian MMM with log-normal ROI priors using Meridian's MCMC sampler (5 chains × 2 000 posterior draws) |
| `03_model_diagnostics` | Checks convergence (trace plots, R-hat ≤ 1.1), plots contribution waterfall, ROI bar chart, response curves, adstock decay |
| `04_budget_optimization` | Re-allocates the existing budget to maximise revenue; spend constraints are derived dynamically from actual channel spend |
| `05_synthetic_validation` | Generates data with known ground-truth ROIs, fits the model, and verifies recovery accuracy |
| `06_attribution_validation` | Compares Meridian's estimated ROI against known ground-truth values to quantify model accuracy |

---

## Key Design Decisions

- **Dynamic column detection** — media, impression, and KPI columns are inferred from column names rather than hardcoded, making the pipeline portable across datasets.
- **Dynamic date ranges** — optimization period and summary reports use `data['date'].min()/max()` instead of hardcoded strings.
- **VIF excludes the time index** — the synthetic `t` column is dropped before VIF calculation to avoid spurious multicollinearity.
- **Controls guarded** — `Offline Discount` is only passed to Meridian if the column exists in the loaded data.

---

## Quick Start (Google Colab)

```python
# 1. Install dependencies
!pip install git+https://github.com/google/meridian.git altair -q

# 2. Mount Drive and upload your CSV
from google.colab import drive
drive.mount('/content/drive')

# 3. Run notebooks in order: 01 → 02 → 03 → 04 → 05 → 06
```

---

## Outputs

| File | Description |
|------|-------------|
| `outputs/summary_output.html` | Meridian Marketing Mix Modeling Report — model fit, channel contribution waterfall, ROI bar chart, response curves |
| `outputs/optimization_output.html` | MMM Optimization Report — budget reallocation scenario with ±30% channel constraints |
| `images/rhat_convergence.png` | R-hat convergence diagnostic (all chains ≤ 1.1, confirming MCMC convergence) |
| `images/visualization_2.png` | Additional model diagnostics chart |

---

## Results

**Model fit** — R²: 0.30 · MAPE: 9%

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

`Python` · `Google Meridian` · `TensorFlow Probability` · `ArviZ` · `pandas` · `seaborn` · `statsmodels`