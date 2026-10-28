
import random
import csv
from datetime import date, timedelta
from pathlib import Path
from faker import Faker

SEED = 20261022
random.seed(SEED)
Faker.seed(SEED)
fake = Faker()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

CHANNELS = [
    "Email", "Social Media", "Paid Search", "Organic Search",
    "Display Ads", "Affiliate", "Events", "Direct Mail",
]

TOUCH_TYPES = [
    "ad_click", "email_open", "email_click",
    "web_visit", "event_attendance", "direct_mail",
]


def write_csv(filename, rows, fieldnames):
    path = DATA_DIR / filename

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {filename}: {len(rows):,} records")


def generate_channels():
    return [
        {"channel_id": f"CH-{i:03d}", "channel_name": name}
        for i, name in enumerate(CHANNELS, start=1)
    ]


def generate_campaigns(channels, count=500):
    campaigns = []

    for i in range(1, count + 1):
        start = fake.date_between(
            start_date="-2y", end_date="-30d"
        )
        end = fake.date_between(
            start_date=start, end_date="+90d"
        )

        campaigns.append({
            "campaign_id": f"CMP-2026-{i:06d}",
            "campaign_name": f"{random.choice(CHANNELS)} Campaign {i:04d}",
            "channel_id": random.choice(channels)["channel_id"],
            "budget": round(random.uniform(10000, 500000), 2),
            "currency": "INR",
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
        })

    return campaigns


def generate_contacts(count=50_000):
    contacts = []

    for i in range(1, count + 1):
        created = fake.date_between(
            start_date=date(2023, 1, 1),
            end_date=date(2024, 1, 1),
        )

        contacts.append({
            "contact_id": f"CON-{i:06d}",
            "created_at": created.isoformat(),
        })

    return contacts


def generate_touchpoints(contacts, campaigns, count=200_000):
    touchpoints = []

    for i in range(1, count + 1):
        contact = random.choice(contacts)
        campaign = random.choice(campaigns)

        start = date.fromisoformat(campaign["start_date"])
        end = date.fromisoformat(campaign["end_date"])

        # Select a date inside the campaign's active period.
        days_active = (end - start).days
        touch_date = start + timedelta(
            days=random.randint(0, days_active)
        )

        touch_time = (
            f"{touch_date.isoformat()}T"
            f"{random.randint(0, 23):02d}:"
            f"{random.randint(0, 59):02d}:"
            f"{random.randint(0, 59):02d}"
        )

        touchpoints.append({
            "touchpoint_id": f"TOUCH-{i:06d}",
            "contact_id": contact["contact_id"],
            "campaign_id": campaign["campaign_id"],
            "touchpoint_time": touch_time,
            "touch_type": random.choice(TOUCH_TYPES),
        })

    return touchpoints


def generate_web_sessions(contacts, count=30_000):
    sessions = []

    for i in range(1, count + 1):
        # Some sessions are anonymous visitors.
        if random.random() < 0.20:
            contact_id = ""
            anonymous_id = f"ANON-{i:06d}"
        else:
            contact_id = random.choice(contacts)["contact_id"]
            anonymous_id = ""

        session_date = fake.date_between(
            start_date="-2y",
            end_date="today",
        )

        sessions.append({
            "session_id": f"SES-2026-{i:06d}",
            "contact_id": contact_id,
            "session_time": (
                f"{session_date.isoformat()}T"
                f"{random.randint(0, 23):02d}:"
                f"{random.randint(0, 59):02d}:00"
            ),
            "anonymous_id": anonymous_id,
        })

    return sessions


def generate_leads(contacts, count=10_000):
    leads = []
    statuses = ["new", "qualified", "disqualified", "converted"]

    selected_contacts = random.sample(
        contacts, min(count, len(contacts))
    )

    for i, contact in enumerate(selected_contacts, start=1):
        lead_date = fake.date_between(
            start_date="-2y",
            end_date="today",
        )

        leads.append({
            "lead_id": f"LEAD-2026-{i:06d}",
            "contact_id": contact["contact_id"],
            "created_at": lead_date.isoformat(),
            "lead_status": random.choice(statuses),
        })

    return leads



def generate_opportunities(leads, count=10_000):
    opportunities = []
    selected_leads = random.sample(
        leads, min(count, len(leads))
    )

    for i, lead in enumerate(selected_leads, start=1):
        created_date = date.fromisoformat(lead["created_at"])
        closed_date = created_date + timedelta(
            days=random.randint(7, 120)
        )

        status = random.choices(
            ["won", "lost", "open"],
            weights=[0.45, 0.30, 0.25],
            k=1,
        )[0]

        # Only won opportunities generate revenue.
        revenue = (
            round(random.uniform(5_000, 250_000), 2)
            if status == "won"
            else 0.0
        )

        opportunities.append({
            "opportunity_id": f"OPP-2026-{i:06d}",
            "lead_id": lead["lead_id"],
            "created_at": created_date.isoformat(),
            "closed_at": (
                closed_date.isoformat()
                if status in ["won", "lost"]
                else ""
            ),
            "opportunity_status": status,
            "currency": "INR",
            "revenue": revenue,
        })

    return opportunities


def generate_orders(opportunities):
    orders = []

    for opportunity in opportunities:
        if opportunity["opportunity_status"] == "won":
            orders.append({
                "order_id": f"ORD-2026-{len(orders) + 1:06d}",
                "opportunity_id": opportunity["opportunity_id"],
                "order_time": opportunity["closed_at"],
                "amount": opportunity["revenue"],
                "currency": opportunity["currency"],
            })

    return orders



def generate_cost_records(campaigns):
    cost_records = []
    cost_number = 1

    for campaign in campaigns:
        start_date = date.fromisoformat(campaign["start_date"])
        end_date = date.fromisoformat(campaign["end_date"])

        # Generate three cost records per campaign.
        for cost_type in ["advertising", "creative", "agency"]:
            cost_date = start_date + timedelta(
                days=random.randint(0, (end_date - start_date).days)
            )

            # Allocate the campaign budget across its cost records.
            amount = round(float(campaign["budget"]) / 3, 2)

            cost_records.append({
                "cost_id": f"COST-2026-{cost_number:06d}",
                "campaign_id": campaign["campaign_id"],
                "cost_date": cost_date.isoformat(),
                "amount": amount,
                "currency": campaign["currency"],
                "cost_type": cost_type,
            })

            cost_number += 1

    return cost_records




def generate_attribution_results(opportunities, leads, touchpoints):
    results = []
    lead_by_id = {lead["lead_id"]: lead for lead in leads}

    touches_by_contact = {}
    for touch in touchpoints:
        touches_by_contact.setdefault(
            touch["contact_id"], []
        ).append(touch)

    attribution_number = 1

    for opportunity in opportunities:
        if opportunity["opportunity_status"] != "won":
            continue

        lead = lead_by_id.get(opportunity["lead_id"])
        if not lead or not opportunity["closed_at"]:
            continue

        contact_id = lead["contact_id"]
        conversion_date = opportunity["closed_at"]

        # Compare full timestamps, not just calendar dates.
        eligible = [
            touch
            for touch in touches_by_contact.get(contact_id, [])
            if touch["touchpoint_time"] <= conversion_date
        ]

        if not eligible:
            continue

        eligible.sort(key=lambda touch: touch["touchpoint_time"])

        # Work in integer cents to avoid rounding discrepancies.
        revenue_cents = int(round(float(opportunity["revenue"]) * 100))

        model_allocations = {
            "first_touch": {
                eligible[0]["campaign_id"]: revenue_cents
            },
            "last_touch": {
                eligible[-1]["campaign_id"]: revenue_cents
            },
        }

        # Distribute every cent across touchpoints.
        # Any leftover cents are assigned one at a time.
        linear_allocations = {}
        base_cents, remainder = divmod(
            revenue_cents, len(eligible)
        )

        for index, touch in enumerate(eligible):
            campaign_id = touch["campaign_id"]
            credit_cents = base_cents + (
                1 if index < remainder else 0
            )

            linear_allocations[campaign_id] = (
                linear_allocations.get(campaign_id, 0)
                + credit_cents
            )

        model_allocations["linear"] = linear_allocations

        for model_name, allocations in model_allocations.items():
            for campaign_id, credited_cents in allocations.items():
                results.append({
                    "attribution_id": (
                        f"ATTR-2026-{attribution_number:08d}"
                    ),
                    "opportunity_id": opportunity["opportunity_id"],
                    "campaign_id": campaign_id,
                    "model_name": model_name,
                    "attributed_revenue": credited_cents / 100,
                    "calculated_at": "2026-10-27",
                })
                attribution_number += 1

    return results




def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    channels = generate_channels()
    campaigns = generate_campaigns(channels)
    contacts = generate_contacts()
    touchpoints = generate_touchpoints(contacts, campaigns)
    web_sessions = generate_web_sessions(contacts)
    leads = generate_leads(contacts)
    opportunities = generate_opportunities(leads)
    orders = generate_orders(opportunities)
    cost_records = generate_cost_records(campaigns)
    attribution_results = generate_attribution_results(opportunities, leads, touchpoints)

    write_csv(
        "channels.csv", channels,
        ["channel_id", "channel_name"],
    )

    write_csv(
        "campaigns.csv", campaigns,
        [
            "campaign_id", "campaign_name", "channel_id",
            "budget", "currency", "start_date", "end_date",
        ],
    )

    write_csv(
        "contacts.csv", contacts,
        ["contact_id", "created_at"],
    )

    write_csv(
        "touchpoints.csv", touchpoints,
        [
            "touchpoint_id", "contact_id", "campaign_id",
            "touchpoint_time", "touch_type",
        ],
    )

    
    write_csv(
        "web_sessions.csv",
        web_sessions,
        ["session_id", "contact_id", "session_time", "anonymous_id"],
    )

    write_csv(
        "leads.csv",
        leads,
        ["lead_id", "contact_id", "created_at", "lead_status"],
    )

    
    write_csv(
        "opportunities.csv",
        opportunities,
        [
            "opportunity_id", "lead_id", "created_at",
            "closed_at", "opportunity_status", "currency", "revenue",
        ],
    )

    write_csv(
        "orders.csv",
        orders,
        [
            "order_id", "opportunity_id", "order_time",
            "amount", "currency",
        ],
    )

    
    write_csv(
        "cost_records.csv",
        cost_records,
        [
            "cost_id", "campaign_id", "cost_date",
            "amount", "currency", "cost_type",
        ],
    )

    
    write_csv(
        "attribution_results.csv",
        attribution_results,
        [
            "attribution_id", "opportunity_id", "campaign_id",
            "model_name", "attributed_revenue", "calculated_at",
        ],
    )


    print("\nSynthetic data generation completed!")


if __name__ == "__main__":
    main()
