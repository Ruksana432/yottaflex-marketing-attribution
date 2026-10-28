
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Channel (
    channel_id TEXT PRIMARY KEY,
    channel_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Campaign (
    campaign_id TEXT PRIMARY KEY,
    campaign_name TEXT NOT NULL,
    channel_id TEXT NOT NULL,
    budget REAL NOT NULL CHECK (budget >= 0),
    currency TEXT NOT NULL DEFAULT 'INR',
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    FOREIGN KEY (channel_id) REFERENCES Channel(channel_id),
    CHECK (end_date >= start_date)
);

CREATE TABLE IF NOT EXISTS Contact (
    contact_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Touchpoint (
    touchpoint_id TEXT PRIMARY KEY,
    contact_id TEXT NOT NULL,
    campaign_id TEXT NOT NULL,
    touchpoint_time TEXT NOT NULL,
    touch_type TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES Contact(contact_id),
    FOREIGN KEY (campaign_id) REFERENCES Campaign(campaign_id)
);



-- 5. Creative: advertisement content/design
CREATE TABLE IF NOT EXISTS Creative (
    creative_id TEXT PRIMARY KEY,
    creative_name TEXT NOT NULL,
    creative_type TEXT NOT NULL
);

-- 6. Audience: target customer groups
CREATE TABLE IF NOT EXISTS Audience (
    audience_id TEXT PRIMARY KEY,
    audience_name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- 7. WebSession: website visits
CREATE TABLE IF NOT EXISTS WebSession (
    session_id TEXT PRIMARY KEY,
    contact_id TEXT,
    session_time TEXT NOT NULL,
    anonymous_id TEXT,
    FOREIGN KEY (contact_id) REFERENCES Contact(contact_id)
);

-- 8. Lead: potential customer
CREATE TABLE IF NOT EXISTS Lead (
    lead_id TEXT PRIMARY KEY,
    contact_id TEXT,
    created_at TEXT NOT NULL,
    lead_status TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES Contact(contact_id)
);

-- 9. Opportunity: potential sale
CREATE TABLE IF NOT EXISTS Opportunity (
    opportunity_id TEXT PRIMARY KEY,
    lead_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    closed_at TEXT,
    opportunity_status TEXT NOT NULL,
    currency TEXT NOT NULL DEFAULT 'INR',
    revenue REAL NOT NULL DEFAULT 0 CHECK (revenue >= 0),
    FOREIGN KEY (lead_id) REFERENCES Lead(lead_id),
    CHECK (closed_at IS NULL OR closed_at >= created_at)
);

-- 10. Order: completed purchase
CREATE TABLE IF NOT EXISTS "Order" (
    order_id TEXT PRIMARY KEY,
    opportunity_id TEXT NOT NULL,
    order_time TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    currency TEXT NOT NULL DEFAULT 'INR',
    FOREIGN KEY (opportunity_id) REFERENCES Opportunity(opportunity_id)
);

-- 11. CostRecord: marketing expenses
CREATE TABLE IF NOT EXISTS CostRecord (
    cost_id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    cost_date TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    currency TEXT NOT NULL DEFAULT 'INR',
    cost_type TEXT NOT NULL,
    FOREIGN KEY (campaign_id) REFERENCES Campaign(campaign_id)
);

-- 12. AttributionResult: calculated campaign credit
CREATE TABLE IF NOT EXISTS AttributionResult (
    attribution_id TEXT PRIMARY KEY,
    opportunity_id TEXT NOT NULL,
    campaign_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    attributed_revenue REAL NOT NULL CHECK (attributed_revenue >= 0),
    calculated_at TEXT NOT NULL,
    FOREIGN KEY (opportunity_id) REFERENCES Opportunity(opportunity_id),
    FOREIGN KEY (campaign_id) REFERENCES Campaign(campaign_id),
    UNIQUE (opportunity_id, campaign_id, model_name)
);

-- Bridge table: campaigns can target multiple audiences
CREATE TABLE IF NOT EXISTS CampaignAudience (
    campaign_id TEXT NOT NULL,
    audience_id TEXT NOT NULL,
    PRIMARY KEY (campaign_id, audience_id),
    FOREIGN KEY (campaign_id) REFERENCES Campaign(campaign_id),
    FOREIGN KEY (audience_id) REFERENCES Audience(audience_id)
);

-- Bridge table: campaigns can use multiple creatives
CREATE TABLE IF NOT EXISTS CampaignCreative (
    campaign_id TEXT NOT NULL,
    creative_id TEXT NOT NULL,
    PRIMARY KEY (campaign_id, creative_id),
    FOREIGN KEY (campaign_id) REFERENCES Campaign(campaign_id),
    FOREIGN KEY (creative_id) REFERENCES Creative(creative_id)
);

-- History: retain lead and opportunity status changes
CREATE TABLE IF NOT EXISTS EntityEvent (
    event_id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    old_status TEXT,
    new_status TEXT NOT NULL,
    event_time TEXT NOT NULL,
    reason TEXT
);
