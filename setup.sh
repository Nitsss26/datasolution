#!/bin/bash

echo "🚀 Setting up D2C Analytics Platform..."

# Create necessary directories
mkdir -p credentials
mkdir -p bigquery-data
mkdir -p logs

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOL
# BigQuery Configuration
BIGQUERY_PROJECT_ID=d2c-analytics-local
GOOGLE_APPLICATION_CREDENTIALS=./credentials/bigquery-key.json

# MongoDB Configuration
MONGODB_URL=mongodb://admin:password123@localhost:27017/d2c_analytics?authSource=admin

# Redis Configuration
REDIS_URL=redis://localhost:6379

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Platform API Keys (Optional - for real data)
SHOPIFY_API_KEY=
SHOPIFY_API_SECRET=
FACEBOOK_ACCESS_TOKEN=
GOOGLE_ADS_DEVELOPER_TOKEN=
SHIPROCKET_API_KEY=
EOL
    echo "✅ Created .env file with default values"
else
    echo "⚠️  .env file already exists, skipping..."
fi

# Create BigQuery service account placeholder
if [ ! -f credentials/bigquery-key.json ]; then
    echo "📝 Creating BigQuery credentials placeholder..."
    cat > credentials/bigquery-key.json << EOL
{
  "type": "service_account",
  "project_id": "d2c-analytics-local",
  "private_key_id": "demo",
  "private_key": "-----BEGIN PRIVATE KEY-----\nDEMO_KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "demo@d2c-analytics-local.iam.gserviceaccount.com",
  "client_id": "demo",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
EOL
    echo "✅ Created BigQuery credentials placeholder"
    echo "⚠️  Replace with real credentials for production use"
fi

echo ""
echo "🎯 Setup complete! Next steps:"
echo ""
echo "1. Start the platform:"
echo "   docker-compose up -d"
echo ""
echo "2. Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   MongoDB: localhost:27017"
echo "   Redis: localhost:6379"
echo ""
echo "3. For real data integration:"
echo "   - Add your API credentials to .env file"
echo "   - Replace BigQuery credentials in credentials/bigquery-key.json"
echo ""
echo "4. The platform works in demo mode without any API keys!"
echo ""
echo "🚀 Happy analyzing!"