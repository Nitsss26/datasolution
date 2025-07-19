// MongoDB initialization script
db = db.getSiblingDB('d2c_analytics');

// Create collections
db.createCollection('platform_configs');
db.createCollection('user_preferences');
db.createCollection('sync_logs');
db.createCollection('error_logs');
db.createCollection('integration_configs');

// Create indexes
db.platform_configs.createIndex({ "platform_id": 1 }, { unique: true });
db.sync_logs.createIndex({ "timestamp": -1 });
db.error_logs.createIndex({ "timestamp": -1 });
db.integration_configs.createIndex({ "type": 1 }, { unique: true });

// Insert default configurations
db.platform_configs.insertMany([
    {
        "platform_id": "shopify",
        "platform_name": "Shopify",
        "connected": false,
        "credentials": {},
        "last_sync": null,
        "created_at": new Date(),
        "updated_at": new Date()
    },
    {
        "platform_id": "facebook",
        "platform_name": "Facebook Ads",
        "connected": false,
        "credentials": {},
        "last_sync": null,
        "created_at": new Date(),
        "updated_at": new Date()
    },
    {
        "platform_id": "google",
        "platform_name": "Google Ads",
        "connected": false,
        "credentials": {},
        "last_sync": null,
        "created_at": new Date(),
        "updated_at": new Date()
    },
    {
        "platform_id": "shiprocket",
        "platform_name": "Shiprocket",
        "connected": false,
        "credentials": {},
        "last_sync": null,
        "created_at": new Date(),
        "updated_at": new Date()
    }
]);

// Insert default user preferences
db.user_preferences.insertOne({
    "user_id": "default",
    "selectedPlatforms": ["all"],
    "defaultTimeRange": "30d",
    "favoriteCharts": [],
    "theme": "system",
    "aiEnabled": true,
    "dashboardLayout": [],
    "created_at": new Date(),
    "updated_at": new Date()
});

// Insert default integration settings
db.integration_configs.insertOne({
    "type": "pipeline_settings",
    "config": {
        "auto_sync": true,
        "sync_frequency": "hourly",
        "data_retention_days": 365,
        "enable_real_time": false,
        "batch_size": 1000,
        "error_retry_count": 3,
        "notification_email": "",
        "webhook_url": ""
    },
    "created_at": new Date(),
    "updated_at": new Date()
});

print("✅ MongoDB initialized successfully with default data");