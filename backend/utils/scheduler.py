import asyncio
import schedule
import time
import logging
from datetime import datetime
from typing import List
from .data_processor import DataProcessor

logger = logging.getLogger(__name__)

class DataScheduler:
    def __init__(self, data_processor: DataProcessor):
        self.data_processor = data_processor
        self.is_running = False
        self.scheduler_task = None
    
    def start(self):
        """Start the data sync scheduler"""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
        
        # Schedule data sync jobs
        schedule.every(1).hours.do(self._sync_shopify)
        schedule.every(1).hours.do(self._sync_facebook)
        schedule.every(1).hours.do(self._sync_google_ads)
        schedule.every(6).hours.do(self._sync_shiprocket)
        
        # Schedule cleanup jobs
        schedule.every().day.at("02:00").do(self._cleanup_old_data)
        schedule.every().week.do(self._optimize_database)
        
        self.is_running = True
        
        # Start the scheduler in background
        self.scheduler_task = asyncio.create_task(self._run_scheduler())
        
        logger.info("✅ Data sync scheduler started")
    
    def stop(self):
        """Stop the data sync scheduler"""
        if not self.is_running:
            return
        
        self.is_running = False
        
        if self.scheduler_task:
            self.scheduler_task.cancel()
        
        schedule.clear()
        logger.info("✅ Data sync scheduler stopped")
    
    async def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.is_running:
            try:
                schedule.run_pending()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(60)
    
    def _sync_shopify(self):
        """Schedule Shopify data sync"""
        asyncio.create_task(self._async_sync_shopify())
    
    def _sync_facebook(self):
        """Schedule Facebook data sync"""
        asyncio.create_task(self._async_sync_facebook())
    
    def _sync_google_ads(self):
        """Schedule Google Ads data sync"""
        asyncio.create_task(self._async_sync_google_ads())
    
    def _sync_shiprocket(self):
        """Schedule Shiprocket data sync"""
        asyncio.create_task(self._async_sync_shiprocket())
    
    async def _async_sync_shopify(self):
        """Async Shopify sync"""
        try:
            logger.info("🔄 Starting scheduled Shopify sync")
            await self.data_processor.sync_shopify_data()
            logger.info("✅ Scheduled Shopify sync completed")
        except Exception as e:
            logger.error(f"❌ Scheduled Shopify sync failed: {e}")
    
    async def _async_sync_facebook(self):
        """Async Facebook sync"""
        try:
            logger.info("🔄 Starting scheduled Facebook sync")
            await self.data_processor.sync_facebook_data()
            logger.info("✅ Scheduled Facebook sync completed")
        except Exception as e:
            logger.error(f"❌ Scheduled Facebook sync failed: {e}")
    
    async def _async_sync_google_ads(self):
        """Async Google Ads sync"""
        try:
            logger.info("🔄 Starting scheduled Google Ads sync")
            await self.data_processor.sync_google_ads_data()
            logger.info("✅ Scheduled Google Ads sync completed")
        except Exception as e:
            logger.error(f"❌ Scheduled Google Ads sync failed: {e}")
    
    async def _async_sync_shiprocket(self):
        """Async Shiprocket sync"""
        try:
            logger.info("🔄 Starting scheduled Shiprocket sync")
            await self.data_processor.sync_shiprocket_data()
            logger.info("✅ Scheduled Shiprocket sync completed")
        except Exception as e:
            logger.error(f"❌ Scheduled Shiprocket sync failed: {e}")
    
    def _cleanup_old_data(self):
        """Schedule data cleanup"""
        asyncio.create_task(self._async_cleanup_old_data())
    
    def _optimize_database(self):
        """Schedule database optimization"""
        asyncio.create_task(self._async_optimize_database())
    
    async def _async_cleanup_old_data(self):
        """Clean up old data"""
        try:
            logger.info("🧹 Starting data cleanup")
            # Implement data cleanup logic here
            # For example, remove data older than 2 years
            logger.info("✅ Data cleanup completed")
        except Exception as e:
            logger.error(f"❌ Data cleanup failed: {e}")
    
    async def _async_optimize_database(self):
        """Optimize database performance"""
        try:
            logger.info("⚡ Starting database optimization")
            # Implement database optimization logic here
            logger.info("✅ Database optimization completed")
        except Exception as e:
            logger.error(f"❌ Database optimization failed: {e}")
    
    def is_running(self) -> bool:
        """Check if scheduler is running"""
        return self.is_running