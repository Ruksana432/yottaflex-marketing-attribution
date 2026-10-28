
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_csv(filename):
    path = DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Missing file: {filename}. Run generate_data.py first."
        )

    return pd.read_csv(path, keep_default_na=False)


def check_unique(df, column, label):
    duplicates = df[column].duplicated().sum()
    print(f"{label}: {'PASS' if duplicates == 0 else 'FAIL'} "
          f"({duplicates} duplicate IDs)")
    return duplicates == 0


def check_foreign_key(child, child_col, parent, parent_col, label):
    valid_ids = set(parent[parent_col])
    invalid = (~child[child_col].isin(valid_ids)).sum()

    print(f"{label}: {'PASS' if invalid == 0 else 'FAIL'} "
          f"({invalid} invalid references)")
    return invalid == 0


def main():
    print("YottaFlex Data Validation")
    print("=" * 35)

    channels = load_csv("channels.csv")
    campaigns = load_csv("campaigns.csv")
    contacts = load_csv("contacts.csv")
    touchpoints = load_csv("touchpoints.csv")
    leads = load_csv("leads.csv")
    opportunities = load_csv("opportunities.csv")
    orders = load_csv("orders.csv")
    costs = load_csv("cost_records.csv")
    attribution = load_csv("attribution_results.csv")

    checks = []

    # Primary key checks
    checks.append(check_unique(channels, "channel_id", "Channel IDs"))
    checks.append(check_unique(campaigns, "campaign_id", "Campaign IDs"))
    checks.append(check_unique(contacts, "contact_id", "Contact IDs"))
    checks.append(check_unique(touchpoints, "touchpoint_id", "Touchpoint IDs"))
    checks.append(check_unique(leads, "lead_id", "Lead IDs"))
    checks.append(check_unique(opportunities, "opportunity_id", "Opportunity IDs"))
    checks.append(check_unique(orders, "order_id", "Order IDs"))
    checks.append(check_unique(costs, "cost_id", "Cost IDs"))
    checks.append(check_unique(attribution, "attribution_id", "Attribution IDs"))

    # Foreign key checks
    checks.append(check_foreign_key(
        campaigns, "channel_id", channels, "channel_id",
        "Campaign -> Channel"
    ))
    checks.append(check_foreign_key(
        touchpoints, "contact_id", contacts, "contact_id",
        "Touchpoint -> Contact"
    ))
    checks.append(check_foreign_key(
        touchpoints, "campaign_id", campaigns, "campaign_id",
        "Touchpoint -> Campaign"
    ))
    checks.append(check_foreign_key(
        leads, "contact_id", contacts, "contact_id",
        "Lead -> Contact"
    ))
    checks.append(check_foreign_key(
        opportunities, "lead_id", leads, "lead_id",
        "Opportunity -> Lead"
    ))
    checks.append(check_foreign_key(
        orders, "opportunity_id", opportunities, "opportunity_id",
        "Order -> Opportunity"
    ))
    checks.append(check_foreign_key(
        costs, "campaign_id", campaigns, "campaign_id",
        "Cost -> Campaign"
    ))
    checks.append(check_foreign_key(
        attribution, "opportunity_id", opportunities, "opportunity_id",
        "Attribution -> Opportunity"
    ))
    checks.append(check_foreign_key(
        attribution, "campaign_id", campaigns, "campaign_id",
        "Attribution -> Campaign"
    ))

    # Revenue reconciliation
    won = opportunities[
        opportunities["opportunity_status"] == "won"
    ].copy()

    won["revenue"] = pd.to_numeric(won["revenue"])
    orders["amount"] = pd.to_numeric(orders["amount"])

    order_totals = orders.groupby("opportunity_id")["amount"].sum()

    mismatches = 0
    for _, opportunity in won.iterrows():
        actual = order_totals.get(opportunity["opportunity_id"], 0)
        if abs(actual - opportunity["revenue"]) > 0.01:
            mismatches += 1

    print(
        f"Won opportunity/order reconciliation: "
        f"{'PASS' if mismatches == 0 else 'FAIL'} "
        f"({mismatches} mismatches)"
    )
    checks.append(mismatches == 0)

    # Report record counts
    print("\nRecord counts:")
    for name, df in [
        ("Channels", channels),
        ("Campaigns", campaigns),
        ("Contacts", contacts),
        ("Touchpoints", touchpoints),
        ("Leads", leads),
        ("Opportunities", opportunities),
        ("Orders", orders),
        ("Costs", costs),
        ("Attribution results", attribution),
    ]:
        print(f"{name}: {len(df):,}")

    print("\nOverall result:", "PASS" if all(checks) else "CHECK FAILURES")


if __name__ == "__main__":
    main()
