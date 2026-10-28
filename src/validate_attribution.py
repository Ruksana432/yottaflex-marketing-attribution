
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def main():
    opportunities = pd.read_csv(DATA_DIR / "opportunities.csv")
    attribution = pd.read_csv(DATA_DIR / "attribution_results.csv")
    leads = pd.read_csv(DATA_DIR / "leads.csv")
    touchpoints = pd.read_csv(DATA_DIR / "touchpoints.csv")

    # Keep won opportunities only.
    won = opportunities[
        opportunities["opportunity_status"] == "won"
    ].copy()

    expected = won.set_index("opportunity_id")["revenue"].astype(float)

    # Find the contact associated with each opportunity.
    won_with_contacts = won.merge(
        leads[["lead_id", "contact_id"]],
        on="lead_id",
        how="left"
    )

    # Match each opportunity's contact to their touchpoints.
    candidates = won_with_contacts[
        ["opportunity_id", "contact_id", "closed_at"]
    ].merge(
        touchpoints[["contact_id", "touchpoint_time"]],
        on="contact_id",
        how="inner"
    )

    # A touchpoint is eligible only if it happened by conversion time.
    closed_times = pd.to_datetime(
        candidates["closed_at"], errors="coerce"
    )
    touch_times = pd.to_datetime(
        candidates["touchpoint_time"], errors="coerce"
    )

    eligible_ids = set(
        candidates.loc[
            touch_times.notna()
            & closed_times.notna()
            & (touch_times <= closed_times),
            "opportunity_id"
        ].unique()
    )

    print("Attribution Validation")
    print("=" * 55)
    print(f"Won opportunities: {len(expected)}")
    print(f"Won opportunities with eligible touchpoints: {len(eligible_ids)}")
    print(
        "Won opportunities without eligible touchpoints:",
        len(expected.index.difference(pd.Index(eligible_ids)))
    )

    for model in ["first_touch", "last_touch", "linear"]:
        model_data = attribution[
            attribution["model_name"] == model
        ]

        actual = model_data.groupby("opportunity_id")[
            "attributed_revenue"
        ].sum()

        missing_ids = expected.index.difference(actual.index)
        common_ids = expected.index.intersection(actual.index)

        # Separate expected exclusions from genuine missing attribution.
        missing_but_eligible = [
            opp_id for opp_id in missing_ids
            if opp_id in eligible_ids
        ]
        missing_without_eligible = [
            opp_id for opp_id in missing_ids
            if opp_id not in eligible_ids
        ]

        differences = (
            expected.loc[common_ids] - actual.loc[common_ids]
        ).abs()

        mismatch_ids = differences[differences > 0.01].index

        print(f"\nModel: {model}")
        print(f"Missing attribution records: {len(missing_ids)}")
        print(
            "Missing with eligible touchpoints (errors):",
            len(missing_but_eligible)
        )
        print(
            "Missing without eligible touchpoints (excluded):",
            len(missing_without_eligible)
        )
        print(f"Revenue mismatches: {len(mismatch_ids)}")

        if missing_but_eligible:
            print(
                "Example missing despite eligible touchpoints:",
                missing_but_eligible[:5]
            )

        if len(mismatch_ids):
            sample = pd.DataFrame({
                "expected_revenue": expected.loc[mismatch_ids],
                "attributed_revenue": actual.loc[mismatch_ids],
                "difference": differences.loc[mismatch_ids],
            })
            print("Example revenue mismatches:")
            print(sample.head(5).to_string())

    print("\nValidation complete.")


if __name__ == "__main__":
    main()
