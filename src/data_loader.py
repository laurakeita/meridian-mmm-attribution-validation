import pandas as pd
import numpy as np
from meridian.data import load


def load_data(filepath: str) -> pd.DataFrame:
    data = pd.read_csv(filepath, on_bad_lines="skip")

    try:
        data["date"] = pd.to_datetime(data["date"], format="%Y/%m/%d", errors="coerce")
    except Exception:
        data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data.dropna(subset=["date"])

    return data


def detect_columns(data: pd.DataFrame):
    media = [
        col for col in data.columns
        if any(k in col.lower() for k in ["spend", "cost", "budget"])
        and data[col].sum() > 0
    ]
    impressions = [
        col for col in data.columns
        if "impression" in col.lower() or "impresseion" in col.lower()
    ]
    output = [col for col in data.columns if "revenue" in col.lower()]
    return media, impressions, output


def build_channel_mappings(media: list, impressions: list):
    def strip_suffix(col, suffixes):
        for s in suffixes:
            if col.lower().endswith(s):
                return col[: -len(s)]
        return col

    cost_mapping = {col: strip_suffix(col, ["spend", "cost", "budget"]) for col in media}
    impressions_mapping = {col: strip_suffix(col, ["impression", "impresseion"]) for col in impressions}
    return cost_mapping, impressions_mapping


def build_meridian_dataset(data: pd.DataFrame, media: list, impressions: list,
                           output: list, cost_mapping: dict, impressions_mapping: dict):
    controls_candidates = ["Offline Discount"]
    controls = [c for c in controls_candidates if c in data.columns]

    coord_to_columns = load.CoordToColumns(
        time="date",
        kpi=output[0],
        controls=controls if controls else None,
        media=impressions,
        media_spend=media,
    )

    loader = load.DataFrameDataLoader(
        df=data,
        kpi_type="revenue",
        coord_to_columns=coord_to_columns,
        media_spend_to_channel=cost_mapping,
        media_to_channel=impressions_mapping,
    )
    return loader.load()
