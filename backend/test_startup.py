#!/usr/bin/env python3
"""
Simple test script to verify backend can start without errors
"""
import sys
import os
import logging

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all modules can be imported without errors"""
    try:
        logger.info("Testing BigQuery client...")
        from utils.bigquery_client import BigQueryClient
        bq_client = BigQueryClient()
        logger.info(f"✅ BigQuery client initialized (connected: {bq_client.is_connected()})")
        
        logger.info("Testing Shopify client...")
        from integrations.shopify_client import ShopifyClient
        shopify_client = ShopifyClient()
        logger.info(f"✅ Shopify client initialized (connected: {shopify_client.is_connected})")
        
        logger.info("Testing Facebook client...")
        from integrations.facebook_client import FacebookClient
        facebook_client = FacebookClient()
        logger.info(f"✅ Facebook client initialized (connected: {facebook_client.is_connected})")
        
        logger.info("Testing Google Ads client...")
        from integrations.google_ads_client import GoogleAdsClient
        google_client = GoogleAdsClient()
        logger.info(f"✅ Google Ads client initialized (connected: {google_client.is_connected})")
        
        logger.info("Testing Shiprocket client...")
        from integrations.shiprocket_client import ShiprocketClient
        shiprocket_client = ShiprocketClient()
        logger.info(f"✅ Shiprocket client initialized (connected: {shiprocket_client.is_connected})")
        
        logger.info("Testing data processor...")
        from utils.data_processor import DataProcessor
        data_processor = DataProcessor(bq_client)
        logger.info("✅ Data processor initialized")
        
        logger.info("Testing router imports...")
        from routers import shopify, facebook_ads, google_ads, shiprocket, analytics
        logger.info("✅ All routers imported successfully")
        
        logger.info("🎉 All imports successful! Backend should start without errors.")
        return True
        
    except Exception as e:
        logger.error(f"❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)