import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any
from .data_processor import DataProcessor

logger = logging.getLogger(__name__)

class DataScheduler:
    def __init__(self, data_processor: DataProcessor):
        self.data_processor = data_processor
        self.is_running = False
        self.task = None
        self.sync_interval = 3600  # 1 hour in seconds
        
    def start(self):
        """Start the data sync scheduler"""
        if not self.is_running:
            self.is_running = True
            self.task = asyncio.create_task(self._scheduler_loop())
            logger.info("✅ Data sync scheduler started")
    
    def stop(self):
        """Stop the data sync scheduler"""
        if self.is_running:
            self.is_running = False
            if self.task:
                self.task.cancel()
            logger.info("⏹️ Data sync scheduler stopped")
    
    def is_running_status(self) -> bool:
        """Check if scheduler is running"""
        return self.is_running
    
    async def _scheduler_loop(self):
        """Main scheduler loop"""
        while self.is_running:
            try:
                logger.info("🔄 Starting scheduled data sync...")
                
                # Sync all platforms
                platforms = ["shopify", "facebook", "google", "shiprocket"]
                await self.data_processor.sync_all_platforms(platforms, force_refresh=False)
                
                logger.info("✅ Scheduled data sync completed")
                
                # Wait for next sync
                await asyncio.sleep(self.sync_interval)
                
            except asyncio.CancelledError:
                logger.info("📋 Scheduler task cancelled")
                break
            except Exception as e:
                logger.error(f"❌ Scheduler error: {e}")
                # Wait a bit before retrying
                await asyncio.sleep(300)  # 5 minutes
    
    def set_sync_interval(self, interval_seconds: int):
        """Set sync interval in seconds"""
        self.sync_interval = max(300, interval_seconds)  # Minimum 5 minutes
        logger.info(f"📅 Sync interval set to {self.sync_interval} seconds")