# Data Dictionary — Marketing Attribution

## Overview

This document describes the main entities used in the synthetic marketing attribution dataset. The dataset supports campaign ROI analysis, attribution modeling, and data-quality anomaly detection.

## Tables and Columns

| Entity / CSV | Important columns | Description |
|---|---|---|
| `channels.csv` | `channel_id`, `channel_name` | Marketing channels such as Email, Paid Search, and Social Media. |
| `campaigns.csv` | `campaign_id`, `campaign_name`, `channel_id`, `currency` | Campaign metadata and its associated marketing channel. |
| `contacts.csv` | `contact_id` and contact attributes | Synthetic people or organizations interacting with marketing campaigns. |
| `touchpoints.csv` | `touchpoint_id`, `contact_id`, `campaign_id`, `touchpoint_time` | Marketing interactions used by attribution models. |
| `web_sessions.csv` | Session identifiers and session attributes | Synthetic website session activity. |
| `leads.csv` | `lead_id`, `contact_id` | Lead records linked to contacts. |
| `opportunities.csv` | `opportunity_id`, `lead_id`, `opportunity_status`, `revenue`, `closed_at` | Sales opportunities, outcomes, revenue, and conversion timing. |
| `orders.csv` | Order identifiers, opportunity references, and order values | Orders associated with won opportunities. |
| `cost_records.csv` | Cost identifiers, `campaign_id`, `amount`, `currency` | Marketing spend associated with campaigns. |
| `attribution_results.csv` | `attribution_id`, `opportunity_id`, `campaign_id`, `model_name`, `attributed_revenue` | Revenue credit assigned to campaigns under each attribution model. |

**Note:** Confirm exact column names against the generated CSV headers and `src/schema.sql` before treating this summary as an exhaustive schema reference.

## Attribution Models

### First-touch
Assigns the opportunity's revenue to the earliest eligible touchpoint's campaign.

### Last-touch
Assigns the opportunity's revenue to the latest eligible touchpoint's campaign.

### Linear
Distributes the opportunity's revenue equally across eligible touchpoints. Credit from repeated campaigns is combined.

## Eligibility Rules

- Only won opportunities are included in the current attribution results.
- Touchpoints must occur on or before the opportunity's conversion timestamp.
- Won opportunities without eligible touchpoints are excluded rather than assigned to an invented campaign.
- Revenue allocation is calculated in cents to avoid rounding discrepancies.

## Data Quality and Anomaly Scenarios

The anomaly-testing pipeline includes five labeled scenarios:

1. Duplicate revenue
2. Post-conversion touchpoint
3. Currency mismatch
4. Missing campaign costs
5. Unsupported identity link

Ground-truth labels are stored separately from detected findings under `data/anomalous/`.

## Reproducibility

The synthetic data generator uses seed `20261022`. See the root `README.md` for setup, generation, loading, validation, reporting, and anomaly-evaluation commands.
