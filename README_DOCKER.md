# Docker Setup for AdsGenerator

## Prerequisites

- Docker and Docker Compose installed
- `.env` file with required API keys (see `.env.example`)

## Quick Start

1. **Create `.env` file** (copy from `.env.example` if available):
   ```bash
   # Required
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # Optional (for notifications)
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   TWILIO_PHONE_NUMBER=your_twilio_phone
   SENDGRID_API_KEY=your_sendgrid_key
   
   # Database (optional, defaults shown)
   DB_NAME=adsgenerator
   DB_USER=postgres
   DB_PASSWORD=postgres
   
   # Secret key (change in production)
   SECRET_KEY=your-secret-key-here
   ```

2. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

   This will start:
   - PostgreSQL database (port 5432)
   - Redis queue (port 6379)
   - Web application (port 5001)
   - Background worker for jobs

3. **Access the application**:
   Open your browser to: http://localhost:5001

## Using Docker Commands Directly

If you prefer using Docker commands directly instead of docker-compose:

1. **Build the image**:
   ```bash
   docker build -t adsgenerator .
   ```

2. **Run PostgreSQL**:
   ```bash
   docker run -d --name adsgenerator_db \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=postgres \
     -e POSTGRES_DB=adsgenerator \
     -p 5432:5432 \
     postgres:15-alpine
   ```

3. **Run Redis**:
   ```bash
   docker run -d --name adsgenerator_redis \
     -p 6379:6379 \
     redis:7-alpine
   ```

4. **Initialize database schema**:
   ```bash
   # Wait a few seconds for postgres to start, then:
   docker exec -i adsgenerator_db psql -U postgres -d adsgenerator < database/schema.sql
   ```

5. **Run the application**:
   ```bash
   docker run -d --name adsgenerator_web \
     --link adsgenerator_db:db \
     --link adsgenerator_redis:redis \
     -e DB_HOST=db \
     -e DB_PORT=5432 \
     -e DB_NAME=adsgenerator \
     -e DB_USER=postgres \
     -e DB_PASSWORD=postgres \
     -e REDIS_URL=redis://redis:6379/0 \
     -e GEMINI_API_KEY=your_gemini_api_key \
     -p 5001:5001 \
     adsgenerator
   ```

6. **Run the worker** (in a separate terminal):
   ```bash
   docker run -d --name adsgenerator_worker \
     --link adsgenerator_db:db \
     --link adsgenerator_redis:redis \
     -e DB_HOST=db \
     -e DB_PORT=5432 \
     -e DB_NAME=adsgenerator \
     -e DB_USER=postgres \
     -e DB_PASSWORD=postgres \
     -e REDIS_URL=redis://redis:6379/0 \
     -e GEMINI_API_KEY=your_gemini_api_key \
     adsgenerator python run_worker.py
   ```

## Environment Variables

The application supports the following environment variables:

- `GEMINI_API_KEY` (required): Google Gemini API key
- `DB_HOST`: PostgreSQL host (default: localhost)
- `DB_PORT`: PostgreSQL port (default: 5432)
- `DB_NAME`: Database name (default: adsgenerator)
- `DB_USER`: Database user (default: postgres)
- `DB_PASSWORD`: Database password (default: postgres)
- `REDIS_URL`: Redis connection URL (default: redis://localhost:6379/0)
- `TWILIO_ACCOUNT_SID`: Twilio account SID (optional)
- `TWILIO_AUTH_TOKEN`: Twilio auth token (optional)
- `TWILIO_PHONE_NUMBER`: Twilio phone number (optional)
- `SENDGRID_API_KEY`: SendGrid API key (optional)
- `SECRET_KEY`: Flask secret key (change in production)

## Database Schema

The database schema is automatically initialized when using docker-compose (via the `schema.sql` file mounted as an init script).

The schema includes:
- `campaigns`: Campaign metadata
- `ad_variants`: Generated ad variations
- `recipients`: Email/SMS recipients
- `sends`: Individual send tracking
- `events`: Analytics events (opens, clicks, bounces, etc.)

## Stopping Services

To stop all services:
```bash
docker-compose down
```

To stop and remove volumes (deletes database data):
```bash
docker-compose down -v
```

## Troubleshooting

1. **Database connection errors**: Ensure PostgreSQL container is healthy before starting the web app
2. **Redis connection errors**: Ensure Redis container is running
3. **Port conflicts**: Change port mappings in `docker-compose.yml` if ports 5001, 5432, or 6379 are in use
4. **Environment variables**: Ensure `.env` file exists and contains required keys

