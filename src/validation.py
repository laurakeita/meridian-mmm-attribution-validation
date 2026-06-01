import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.outliers_influence import variance_inflation_factor


def spend_share_analysis(data: pd.DataFrame, media: list):
    total = data[media].sum().sum()
    share = (data[media].sum() / total).reset_index()
    share.columns = ["Media_Channel", "Spend_Share"]

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="Spend_Share", y="Media_Channel",
                data=share.sort_values("Spend_Share", ascending=False), ax=ax)
    ax.set_title("Spend Share by Media Channel")
    plt.tight_layout()
    plt.show()
    return share


def correlation_analysis(data: pd.DataFrame, revenue_col: str, top_n: int = 10):
    numeric = data.select_dtypes(include=[np.number])
    corr = numeric.corr()[revenue_col].drop(labels=[revenue_col]).sort_values(ascending=False)

    top_features = corr.abs().sort_values(ascending=False).head(top_n).index.tolist() + [revenue_col]
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(numeric[top_features].corr(), annot=True, cmap="coolwarm", center=0, ax=ax)
    ax.set_title(f"Top {top_n} Features Correlated with {revenue_col}")
    plt.tight_layout()
    plt.show()
    return corr


def vif_analysis(X: pd.DataFrame) -> pd.DataFrame:
    X_numeric = X.select_dtypes(include=[np.number]).drop(columns=["t"], errors="ignore")
    if X_numeric.empty:
        print("No numeric features for VIF analysis.")
        return pd.DataFrame()

    vif_df = pd.DataFrame({
        "Feature": X_numeric.columns,
        "VIF": [variance_inflation_factor(X_numeric.values, i)
                for i in range(X_numeric.shape[1])],
    })
    return vif_df.sort_values("VIF", ascending=False)


def check_data_quality(data: pd.DataFrame):
    print("=== Missing Values ===")
    missing = data.isnull().sum()
    print(missing[missing > 0] if missing.any() else "No missing values.")

    print("\n=== Low-record Columns (<15 non-null) ===")
    low = {c: data[c].count() for c in data.columns if data[c].count() < 15}
    print(low if low else "All columns have ≥15 records.")

    print("\n=== Date Range ===")
    if "date" in data.columns:
        print(f"  {data['date'].min().date()} → {data['date'].max().date()}  ({len(data)} rows)")
