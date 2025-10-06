#!/usr/bin/env python
"""
Debug script to check database configuration on Railway
Run this to see what database is being used
"""
import os
import sys
import django

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meal_mate.settings')
django.setup()

from django.conf import settings
from django.db import connection

print("=== DATABASE DEBUG INFO ===")
print(f"DATABASE_URL exists: {bool(os.getenv('DATABASE_URL'))}")
print(f"RAILWAY_ENVIRONMENT: {os.getenv('RAILWAY_ENVIRONMENT')}")
print(f"RAILWAY_PUBLIC_DOMAIN: {os.getenv('RAILWAY_PUBLIC_DOMAIN')}")
print(f"Database Engine: {settings.DATABASES['default']['ENGINE']}")
print(f"Database Name: {settings.DATABASES['default'].get('NAME', 'N/A')}")

# Check if tables exist
with connection.cursor() as cursor:
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'delivery_%';")
        tables = cursor.fetchall()
        print(f"Delivery tables found: {[table[0] for table in tables]}")
    except Exception as e:
        print(f"Error checking tables: {e}")

print("=== END DEBUG INFO ===")
