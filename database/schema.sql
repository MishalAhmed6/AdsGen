-- PostgreSQL Schema for AdsCompetitor Analytics
-- Run this to initialize the database

-- Enable UUID extension if needed
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Campaigns table
CREATE TABLE IF NOT EXISTS campaigns (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    brand_name VARCHAR(255) NOT NULL,
    competitor_name VARCHAR(255) NOT NULL,
    zipcode VARCHAR(20),
    industry VARCHAR(100),
    audience_type VARCHAR(100),
    offer_type VARCHAR(100),
    goal VARCHAR(100),
    scheduled_at TIMESTAMP WITH TIME ZONE,
    timezone VARCHAR(100),
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'scheduled', 'sending', 'completed', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Ad Variants table
CREATE TABLE IF NOT EXISTS ad_variants (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    headline TEXT NOT NULL,
    ad_text TEXT NOT NULL,
    cta TEXT NOT NULL,
    hashtags JSONB DEFAULT '[]'::jsonb,
    quality_score DECIMAL(3, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Recipients table
CREATE TABLE IF NOT EXISTS recipients (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    channel VARCHAR(20) NOT NULL CHECK (channel IN ('sms', 'email')),
    tags JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create unique constraints as partial indexes (PostgreSQL syntax)
CREATE UNIQUE INDEX IF NOT EXISTS recipients_unique_email ON recipients(campaign_id, email) WHERE email IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS recipients_unique_phone ON recipients(campaign_id, phone) WHERE phone IS NOT NULL;

-- Sends table (tracks individual sends)
CREATE TABLE IF NOT EXISTS sends (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    ad_variant_id INTEGER NOT NULL REFERENCES ad_variants(id) ON DELETE CASCADE,
    recipient_id INTEGER NOT NULL REFERENCES recipients(id) ON DELETE CASCADE,
    channel VARCHAR(20) NOT NULL CHECK (channel IN ('sms', 'email')),
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'delivered', 'failed', 'bounced')),
    sent_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Events table (for tracking opens, clicks, bounces, etc.)
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    send_id INTEGER NOT NULL REFERENCES sends(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL CHECK (event_type IN ('send', 'delivery', 'open', 'click', 'bounce', 'failure')),
    event_data JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
CREATE INDEX IF NOT EXISTS idx_campaigns_scheduled_at ON campaigns(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_campaigns_created_at ON campaigns(created_at);

CREATE INDEX IF NOT EXISTS idx_ad_variants_campaign_id ON ad_variants(campaign_id);

CREATE INDEX IF NOT EXISTS idx_recipients_campaign_id ON recipients(campaign_id);
CREATE INDEX IF NOT EXISTS idx_recipients_channel ON recipients(channel);
CREATE INDEX IF NOT EXISTS idx_recipients_email ON recipients(email) WHERE email IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_recipients_phone ON recipients(phone) WHERE phone IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_sends_campaign_id ON sends(campaign_id);
CREATE INDEX IF NOT EXISTS idx_sends_ad_variant_id ON sends(ad_variant_id);
CREATE INDEX IF NOT EXISTS idx_sends_recipient_id ON sends(recipient_id);
CREATE INDEX IF NOT EXISTS idx_sends_status ON sends(status);
CREATE INDEX IF NOT EXISTS idx_sends_channel ON sends(channel);
CREATE INDEX IF NOT EXISTS idx_sends_sent_at ON sends(sent_at);
CREATE INDEX IF NOT EXISTS idx_sends_delivered_at ON sends(delivered_at);

CREATE INDEX IF NOT EXISTS idx_events_send_id ON events(send_id);
CREATE INDEX IF NOT EXISTS idx_events_event_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_created_at ON events(created_at);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at
CREATE TRIGGER update_campaigns_updated_at BEFORE UPDATE ON campaigns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

