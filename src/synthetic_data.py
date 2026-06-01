import numpy as np
import pandas as pd


def generate_synthetic_mmm_data(
    n_weeks: int = 104,
    start_date: str = "2022-01-03",
    seed: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start_date, periods=n_weeks, freq="W-MON")

    # Spend (log-normal)
    meta_spend = rng.lognormal(mean=9.5, sigma=0.4, size=n_weeks)
    google_spend = rng.lognormal(mean=9.8, sigma=0.35, size=n_weeks)

    # Impressions (proportional to spend + noise)
    meta_impressions = meta_spend * rng.uniform(80, 120, n_weeks)
    google_impressions = google_spend * rng.uniform(60, 90, n_weeks)

    # Adstock transform (geometric decay)
    def adstock(x, decay=0.5):
        out = np.zeros_like(x)
        out[0] = x[0]
        for t in range(1, len(x)):
            out[t] = x[t] + decay * out[t - 1]
        return out

    meta_adstock = adstock(meta_impressions, decay=0.4)
    google_adstock = adstock(google_impressions, decay=0.3)

    # Seasonality
    t = np.arange(n_weeks)
    seasonality = 1 + 0.15 * np.sin(2 * np.pi * t / 52) + 0.08 * np.cos(4 * np.pi * t / 52)

    # Offline discount (control)
    offline_discount = rng.choice([0, 0.05, 0.1, 0.15], size=n_weeks, p=[0.6, 0.2, 0.1, 0.1])

    # Revenue
    base = 500_000
    revenue = (
        base
        + 0.8 * meta_adstock
        + 1.2 * google_adstock
        + 200_000 * offline_discount
    ) * seasonality + rng.normal(0, 20_000, n_weeks)
    revenue = np.clip(revenue, 0, None)

    return pd.DataFrame({
        "date": dates.strftime("%Y/%m/%d"),
        "Meta_spend": meta_spend.round(2),
        "Google_spend": google_spend.round(2),
        "Meta_impression": meta_impressions.round(0).astype(int),
        "Google_impression": google_impressions.round(0).astype(int),
        "Offline Discount": offline_discount,
        "Revenue": revenue.round(2),
    })


if __name__ == "__main__":
    df = generate_synthetic_mmm_data()
    df.to_csv("data/synthetic_mmm_data.csv", index=False)
    print(f"Generated {len(df)} rows → data/synthetic_mmm_data.csv")
    print(df.head())
