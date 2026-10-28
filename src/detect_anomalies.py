
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "anomalous"
NORMAL_DATA_DIR = BASE_DIR / "data"


def clean(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def main():
    # Read IDs as strings to avoid mixed-type warnings.
    campaigns = pd.read_csv(
        DATA_DIR / "campaigns.csv", dtype=str, keep_default_na=False
    )
    costs = pd.read_csv(
        DATA_DIR / "cost_records.csv", dtype=str, keep_default_na=False
    )
    orders = pd.read_csv(
        DATA_DIR / "orders.csv", dtype=str, keep_default_na=False
    )
    touches = pd.read_csv(
        DATA_DIR / "touchpoints.csv", dtype=str, keep_default_na=False
    )
    sessions = pd.read_csv(
        DATA_DIR / "web_sessions.csv", dtype=str, keep_default_na=False
    )
    opportunities = pd.read_csv(
        DATA_DIR / "opportunities.csv", dtype=str, keep_default_na=False
    )
    contacts = pd.read_csv(
        NORMAL_DATA_DIR / "contacts.csv",
        dtype=str,
        keep_default_na=False,
    )

    findings = []

    def report(anomaly_type, entity_type, entity_id, reason):
        findings.append({
            "anomaly_type": anomaly_type,
            "entity_type": entity_type,
            "entity_id": clean(entity_id),
            "reason": reason,
        })

    # 1. Duplicate orders: flag only the repeated copy.
    if not orders.empty:
        business_columns = [
            col for col in orders.columns if col != "order_id"
        ]

        if business_columns:
            duplicate_mask = orders.duplicated(
                subset=business_columns, keep="first"
            )

            for _, row in orders.loc[duplicate_mask].iterrows():
                report(
                    "duplicate_revenue",
                    "Order",
                    row["order_id"],
                    "Order repeats an earlier order's business fields",
                )

    # 2. Touchpoints after their specifically associated opportunity closes.
    # Ordinary touchpoints without an opportunity ID are not flagged.
    if (
        "opportunity_id" in touches.columns
        and "opportunity_id" in opportunities.columns
        and "closed_at" in opportunities.columns
    ):
        won_opps = opportunities[
            opportunities["opportunity_status"]
            .str.strip()
            .str.lower()
            .eq("won")
        ].copy()

        won_opps["closed_parsed"] = pd.to_datetime(
            won_opps["closed_at"], errors="coerce", utc=True
        )

        close_dates = (
            won_opps.dropna(subset=["closed_parsed"])
            .drop_duplicates("opportunity_id")
            .set_index("opportunity_id")["closed_parsed"]
            .to_dict()
        )

        touches["touch_parsed"] = pd.to_datetime(
            touches["touchpoint_time"], errors="coerce", utc=True
        )

        for _, touch in touches.iterrows():
            opportunity_id = clean(touch.get("opportunity_id", ""))

            if not opportunity_id:
                continue

            close_time = close_dates.get(opportunity_id)
            touch_time = touch["touch_parsed"]

            if (
                close_time is not None
                and pd.notna(touch_time)
                and touch_time > close_time
            ):
                report(
                    "post_conversion_touchpoint",
                    "Touchpoint",
                    touch["touchpoint_id"],
                    "Touchpoint occurs after its associated won opportunity closed",
                )

    # 3. Cost currency must match its campaign currency.
    campaign_currency = {
        clean(row["campaign_id"]): clean(row["currency"]).upper()
        for _, row in campaigns.iterrows()
    }

    for _, cost in costs.iterrows():
        campaign_id = clean(cost.get("campaign_id", ""))
        actual = clean(cost.get("currency", "")).upper()
        expected = campaign_currency.get(campaign_id, "")

        if expected and actual and actual != expected:
            report(
                "currency_mismatch",
                "CostRecord",
                cost["cost_id"],
                f"Cost currency {actual} differs from campaign currency {expected}",
            )

    # 4. Campaigns without any cost records.
    campaigns_with_costs = {
        clean(value) for value in costs["campaign_id"] if clean(value)
    }

    for _, campaign in campaigns.iterrows():
        campaign_id = clean(campaign["campaign_id"])

        if campaign_id and campaign_id not in campaigns_with_costs:
            report(
                "missing_campaign_costs",
                "Campaign",
                campaign_id,
                "No cost records exist for this campaign",
            )

    # 5. Session contact IDs must exist in the contact dataset.
    known_contacts = {
        clean(value) for value in contacts["contact_id"] if clean(value)
    }

    for _, session in sessions.iterrows():
        contact_id = clean(session.get("contact_id", ""))

        # Empty contact ID is allowed for an anonymous session.
        if contact_id and contact_id not in known_contacts:
            report(
                "unsupported_identity_link",
                "WebSession",
                session["session_id"],
                "Session references a contact absent from the contact dataset",
            )

    result = pd.DataFrame(
        findings,
        columns=[
            "anomaly_type",
            "entity_type",
            "entity_id",
            "reason",
        ],
    )

    output = DATA_DIR / "detected_anomalies.csv"
    result.to_csv(output, index=False)

    print("Anomaly detection completed.")
    print(f"Findings: {len(result)}")
    print(f"Report: {output}")

    if not result.empty:
        print("\nFindings by type:")
        print(result["anomaly_type"].value_counts().to_string())


if __name__ == "__main__":
    main()
