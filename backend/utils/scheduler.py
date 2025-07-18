import asyncio
import logging
from typing import Optional
from datetime import datetime, timedelta
import threading

logger = logging.getLogger(__name__)

class DataScheduler:
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.is_running_flag = False
        self.task = None
        self.sync_interval = 3600  # 1 hour in seconds
    
    def start(self):
        """Start the data sync scheduler"""
        try:
            self.is_running_flag = True
            logger.info("🔄 Data sync scheduler started in demo mode")
            # In demo mode, we don't actually start background tasks
        except Exception as e:
            logger.error(f"❌ Failed to start scheduler: {e}")
    
    def stop(self):
        """Stop the data sync scheduler"""
        try:
            self.is_running_flag = False
            if self.task:
                self.task.cancel()
            logger.info("⏹️ Data sync scheduler stopped")
        except Exception as e:
            logger.error(f"❌ Failed to stop scheduler: {e}")
    
    def is_running(self) -> bool:
        """Check if scheduler is running"""
        return self.is_running_flag
    
    async def _sync_loop(self):
        """Background sync loop"""
        while self.is_running_flag:
            try:
                logger.info("🔄 Running scheduled data sync...")
                await self.data_processor.sync_all_platforms(["all"], force_refresh=False)
                logger.info("✅ Scheduled data sync completed")
            except Exception as e:
                logger.error(f"❌ Scheduled sync failed: {e}")
            
            # Wait for next sync interval
            await asyncio.sleep(self.sync_interval)