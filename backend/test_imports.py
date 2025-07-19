#!/usr/bin/env python3
"""
Test script to identify import issues
"""

print("Testing imports...")

try:
    print("✓ Testing FastAPI...")
    from fastapi import FastAPI
    print("✓ FastAPI imported successfully")
except ImportError as e:
    print(f"✗ FastAPI import failed: {e}")

try:
    print("✓ Testing database...")
    from database import get_database, init_database
    print("✓ Database imports successful")
except ImportError as e:
    print(f"✗ Database import failed: {e}")

try:
    print("✓ Testing models...")
    from models.analytics import AnalyticsData, PlatformData, UserPreferences
    print("✓ Models imported successfully")
except ImportError as e:
    print(f"✗ Models import failed: {e}")

try:
    print("✓ Testing utils...")
    from utils.bigquery_client import BigQueryClient
    from utils.data_processor import DataProcessor
    from utils.scheduler import DataScheduler
    print("✓ Utils imported successfully")
except ImportError as e:
    print(f"✗ Utils import failed: {e}")

# Test individual routers
routers_to_test = [
    'shopify', 'facebook_ads', 'google_ads', 'shiprocket', 
    'analytics', 'ai_insights', 'integrations', 'demo_data', 
    'pipeline', 'auth', 'comprehensive_analytics'
]

for router_name in routers_to_test:
    try:
        print(f"✓ Testing router: {router_name}")
        module = __import__(f'routers.{router_name}', fromlist=[router_name])
        if hasattr(module, 'router'):
            print(f"✓ Router {router_name} imported successfully")
        else:
            print(f"⚠ Router {router_name} missing 'router' attribute")
    except ImportError as e:
        print(f"✗ Router {router_name} import failed: {e}")
    except Exception as e:
        print(f"✗ Router {router_name} error: {e}")

print("Import testing completed!")