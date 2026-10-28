
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

MODELS = ["first_touch", "last_touch", "linear"]


def main():
    campaigns = pd.read_csv(DATA_DIR / "campaigns.csv")
    costs = pd.read_csv(DATA_DIR / "cost_records.csv")
    attribution = pd.read_csv(DATA_DIR / "attribution_results.csv")

    # Calculate total marketing spend per campaign.
    spend = (
        costs.groupby("campaign_id", as_index=False)
        .agg(marketing_cost=("amount", "sum"))
    )

    # Calculate attributed revenue separately for each model.
    revenue = (
        attribution.groupby(
            ["campaign_id", "model_name"], as_index=False
        )
        .agg(attributed_revenue=("attributed_revenue", "sum"))
    )

    # Create every campaign-model combination, including zero-revenue rows.
    campaign_base = campaigns[
        ["campaign_id", "campaign_name", "currency"]
    ].copy()

    model_frame = pd.DataFrame({"model_name": MODELS})
    campaign_base["_key"] = 1
    model_frame["_key"] = 1

    report = campaign_base.merge(model_frame, on="_key").drop(
        columns="_key"
    )

    report = report.merge(spend, on="campaign_id", how="left")

    report = report.merge(
        revenue,
        on=["campaign_id", "model_name"],
        how="left",
    )

    report["marketing_cost"] = report["marketing_cost"].fillna(0)
    report["attributed_revenue"] = (
        report["attributed_revenue"].fillna(0)
    )

    # ROI is undefined when campaign spend is zero.
    report["roi_percent"] = (
        (report["attributed_revenue"] - report["marketing_cost"])
        / report["marketing_cost"].replace(0, float("nan"))
    ) * 100

    report = report.sort_values(
        ["campaign_id", "model_name"]
    ).reset_index(drop=True)

    output = DATA_DIR / "campaign_roi_report.csv"
    report.to_csv(output, index=False)

    print(f"ROI report created: {output}")
    print(f"Report rows: {len(report):,}")
    print(f"Expected rows: {len(campaigns) * len(MODELS):,}")
    print(f"Unique campaigns: {report['campaign_id'].nunique():,}")
    print("\nRows per attribution model:")
    print(report["model_name"].value_counts().to_string())
    print("\nSample rows:")
    print(report.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
