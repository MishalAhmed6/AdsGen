#!/usr/bin/env python3
"""
RQ Worker script to process background jobs.
Run this script to start processing queued jobs for AI generation and notifications.

Usage:
    python run_worker.py

Make sure Redis is running before starting the worker.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded environment variables from: {env_path}")
except ImportError:
    pass

from rq import Worker
from jobs.queue_manager import redis_conn, init_queue

if __name__ == '__main__':
    print("=" * 60)
    print("AdsCompetitor Background Job Worker")
    print("=" * 60)
    
    # Initialize queue (this sets the global redis_conn)
    if not init_queue():
        print("\nERROR: Redis connection failed. Please ensure Redis is running.")
        print("Install Redis: https://redis.io/download")
        print("Or start Redis: redis-server")
        sys.exit(1)
    
    # Re-import redis_conn after init_queue sets it
    from jobs.queue_manager import redis_conn
    
    # Verify connection exists
    if redis_conn is None:
        print("\nERROR: Redis connection is None. Please check Redis configuration.")
        print(f"REDIS_URL env: {os.getenv('REDIS_URL')}")
        sys.exit(1)
    
    # Start worker
    print("\nStarting worker...")
    print("Listening for jobs on queue: ads_generator")
    print("Press Ctrl+C to stop the worker")
    print("=" * 60)
    
    # Create worker with connection (newer RQ versions don't use Connection context manager)
    worker = Worker(['ads_generator'], connection=redis_conn)
    worker.work()

