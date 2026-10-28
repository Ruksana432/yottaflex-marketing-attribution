
import random
import shutil
from pathlib import Path

import pandas as pd

SEED = 20261022
random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ANOMALY_DIR = DATA_DIR / "anomalous"


def main():
    ANOMALY_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        "campaigns.csv",
        "touchpoints.csv",
        "opportunities.csv",
        "cost_records.csv",
        "web_sessions.csv",
        "orders.csv",
        "leads.csv",
    ]

    for filename in required_files:
        source = DATA_DIR / filename
        if not source.exists():
            raise FileNotFoundError(f"Missing file: {source}")
        shutil.copy2(source, ANOMALY_DIR / filename)

    campaigns = pd.read_csv(ANOMALY_DIR / "campaigns.csv")
    touches = pd.read_csv(ANOMALY_DIR / "touchpoints.csv")
    opportunities = pd.read_csv(ANOMALY_DIR / "opportunities.csv")
    costs = pd.read_csv(ANOMALY_DIR / "cost_records.csv")
    sessions = pd.read_csv(ANOMALY_DIR / "web_sessions.csv")
    orders = pd.read_csv(ANOMALY_DIR / "orders.csv")

    labels = []

    # 1. Duplicate revenue: duplicate an order row.
    if not orders.empty:
        row = orders.iloc[0].copy()
        duplicate_id = f"ORD-ANOM-{SEED}"
        row["order_id"] = duplicate_id
        orders = pd.concat([orders, pd.DataFrame([row])], ignore_index=True)

        labels.append({
            "anomaly_id": "ANOM-001",
            "anomaly_type": "duplicate_revenue",
            "entity_type": "Order",
            "entity_id": duplicate_id,
            "expected_detection": "Duplicate order for same opportunity and amount",
        })

    # 2. Touchpoint after conversion.
    won = opportunities[
        (opportunities["opportunity_status"] == "won")
        & (opportunities["closed_at"].notna())
        & (opportunities["closed_at"].astype(str) != "")
    ]

    if not won.empty:
        opportunity = won.iloc[0]
        matching = touches[
            touches["contact_id"].isin(
                opportunities.loc[
                    opportunities["opportunity_id"]
                    == opportunity["opportunity_id"],
                    "opportunity_id",
                ]
            )
        ]

        # Find the corresponding lead/contact via the leads file.
        leads = pd.read_csv(ANOMALY_DIR / "leads.csv")
        lead = leads[
            leads["lead_id"] == opportunity["lead_id"]
        ]

        if not lead.empty:
            contact_id = lead.iloc[0]["contact_id"]
            campaign_id = campaigns.iloc[0]["campaign_id"]
            future_date = (
                pd.Timestamp(opportunity["closed_at"])
                + pd.Timedelta(days=10)
            ).strftime("%Y-%m-%dT12:00:00")

            new_touch = {
                "touchpoint_id": f"TOUCH-ANOM-{SEED}",
                "contact_id": contact_id,
                "campaign_id": campaign_id,
                "opportunity_id": opportunity["opportunity_id"],
                "touchpoint_time": future_date,
                "touch_type": "ad_click",
            }
            touches = pd.concat(
                [touches, pd.DataFrame([new_touch])],
                ignore_index=True,
            )

            labels.append({
                "anomaly_id": "ANOM-002",
                "anomaly_type": "post_conversion_touchpoint",
                "entity_type": "Touchpoint",
                "entity_id": new_touch["touchpoint_id"],
                "expected_detection": "Touchpoint timestamp is after opportunity conversion",
            })

    # 3. Currency mismatch: change one cost currency.
    if not costs.empty:
        costs.loc[0, "currency"] = "USD"
        labels.append({
            "anomaly_id": "ANOM-003",
            "anomaly_type": "currency_mismatch",
            "entity_type": "CostRecord",
            "entity_id": costs.loc[0, "cost_id"],
            "expected_detection": "Cost currency differs from its campaign currency",
        })

    # 4. Missing costs: remove all costs for one campaign.
    if not campaigns.empty:
        missing_campaign = campaigns.iloc[-1]["campaign_id"]
        removed = costs[costs["campaign_id"] == missing_campaign]
        costs = costs[costs["campaign_id"] != missing_campaign]

        labels.append({
            "anomaly_id": "ANOM-004",
            "anomaly_type": "missing_campaign_costs",
            "entity_type": "Campaign",
            "entity_id": missing_campaign,
            "expected_detection": f"No cost records remain for this campaign; removed {len(removed)}",
        })

    # 5. Unsupported identity link: assign a contact to an anonymous session.
    anonymous = sessions[
        sessions["contact_id"].isna()
        | (sessions["contact_id"].astype(str) == "")
    ]

    if not anonymous.empty:
        idx = anonymous.index[0]
        sessions.loc[idx, "contact_id"] = "CON-UNVERIFIED"
        labels.append({
            "anomaly_id": "ANOM-005",
            "anomaly_type": "unsupported_identity_link",
            "entity_type": "WebSession",
            "entity_id": sessions.loc[idx, "session_id"],
            "expected_detection": "Session linked to a contact ID without identity evidence",
        })

    campaigns.to_csv(ANOMALY_DIR / "campaigns.csv", index=False)
    touches.to_csv(ANOMALY_DIR / "touchpoints.csv", index=False)
    opportunities.to_csv(ANOMALY_DIR / "opportunities.csv", index=False)
    costs.to_csv(ANOMALY_DIR / "cost_records.csv", index=False)
    sessions.to_csv(ANOMALY_DIR / "web_sessions.csv", index=False)
    orders.to_csv(ANOMALY_DIR / "orders.csv", index=False)

    # Keep ground truth separate from the feature datasets.
    pd.DataFrame(labels).to_csv(
        ANOMALY_DIR / "ground_truth.csv", index=False
    )

    print("Anomaly dataset created:", ANOMALY_DIR)
    print("Ground-truth labels:", len(labels))
    print(pd.DataFrame(labels)[["anomaly_id", "anomaly_type"]].to_string(index=False))


if __name__ == "__main__":
    main()
