# Database Setup for Analytics

## Overview

The application now includes a PostgreSQL database for analytics tracking. This enables:
- Campaign tracking and management
- Ad variant storage
- Recipient management
- Send tracking with delivery status
- Event tracking (sends, deliveries, opens, clicks, bounces)

## Database Schema

### Tables

1. **campaigns** - Stores campaign metadata
   - id, name, brand_name, competitor_name, zipcode
   - industry, audience_type, offer_type, goal
   - scheduled_at, timezone, status
   - created_at, updated_at

2. **ad_variants** - Stores generated ad variations
   - id, campaign_id (FK), headline, ad_text, cta
   - hashtags (JSONB), quality_score
   - created_at

3. **recipients** - Stores email/SMS recipients
   - id, campaign_id (FK), name
   - email, phone, channel (sms/email)
   - tags (JSONB), created_at

4. **sends** - Tracks individual send operations
   - id, campaign_id (FK), ad_variant_id (FK), recipient_id (FK)
   - channel (sms/email), status (pending/sent/delivered/failed/bounced)
   - sent_at, delivered_at, error_message
   - created_at

5. **events** - Tracks analytics events
   - id, send_id (FK), event_type (send/delivery/open/click/bounce/failure)
   - event_data (JSONB), created_at

## Setup Instructions

### Using Docker Compose (Recommended)

1. Create a `.env` file with your database credentials:
   ```bash
   DB_HOST=db
   DB_PORT=5432
   DB_NAME=adsgenerator
   DB_USER=postgres
   DB_PASSWORD=postgres
   ```

2. Run docker-compose:
   ```bash
   docker-compose up
   ```

The schema will be automatically initialized via the `schema.sql` file.

### Manual Setup

1. **Install PostgreSQL** and create a database:
   ```bash
   createdb adsgenerator
   ```

2. **Initialize schema**:
   ```bash
   psql -U postgres -d adsgenerator -f database/schema.sql
   ```

3. **Set environment variables**:
   ```bash
   export DB_HOST=localhost
   export DB_PORT=5432
   export DB_NAME=adsgenerator
   export DB_USER=postgres
   export DB_PASSWORD=your_password
   ```

## Usage

The database integration is **optional** - the application will continue to work without it, but analytics tracking won't be available.

When database is available:
- Campaigns are automatically created when ads are generated
- Ad variants are stored with campaign association
- Recipients are stored when sending
- Sends are tracked with status updates
- Events are logged for analytics

## Querying Analytics

Example queries:

### Get campaign statistics
```sql
SELECT 
    c.id,
    c.name,
    COUNT(DISTINCT s.id) as total_sends,
    COUNT(DISTINCT CASE WHEN s.status = 'delivered' THEN s.id END) as delivered,
    COUNT(DISTINCT CASE WHEN s.status = 'failed' THEN s.id END) as failed
FROM campaigns c
LEFT JOIN sends s ON s.campaign_id = c.id
GROUP BY c.id, c.name;
```

### Get ad performance
```sql
SELECT 
    av.id,
    av.headline,
    COUNT(DISTINCT s.id) as sends,
    COUNT(DISTINCT CASE WHEN s.status = 'delivered' THEN s.id END) as delivered
FROM ad_variants av
LEFT JOIN sends s ON s.ad_variant_id = av.id
WHERE av.campaign_id = 1
GROUP BY av.id, av.headline;
```

### Get event timeline
```sql
SELECT 
    e.event_type,
    COUNT(*) as count,
    DATE_TRUNC('hour', e.created_at) as hour
FROM events e
JOIN sends s ON s.id = e.send_id
WHERE s.campaign_id = 1
GROUP BY e.event_type, hour
ORDER BY hour DESC;
```

## Future Enhancements

- Dashboard UI for viewing analytics
- Click tracking via tracking pixels/URLs
- Open tracking via email pixels
- Bounce handling and recipient cleanup
- Campaign performance comparisons
- A/B testing support

