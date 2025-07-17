# D2C Analytics SaaS - Installation Guide

This guide will help you set up and run the complete D2C Analytics SaaS platform on your Linux virtual machine.

## Prerequisites

- Linux virtual machine (Ubuntu 20.04+ recommended)
- Docker and Docker Compose installed
- Node.js 18+ and npm
- Python 3.11+
- Git

## Project Structure

\`\`\`
datasolution/
├── backend/                 # Python FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── ...
├── app/                     # Next.js frontend
│   ├── page.tsx
│   ├── dashboard/
│   ├── login/
│   └── ...
├── components/              # Shared UI components
└── README.md
\`\`\`

## Installation Steps

### 1. Clone and Setup

\`\`\`bash
# Clone the repository
git clone <your-repo-url>
cd datasolution

# Make setup script executable
chmod +x setup.sh
\`\`\`

### 2. Backend Setup

\`\`\`bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit the .env file with your configurations
nano .env
\`\`\`

### 3. Environment Configuration

Edit the `.env` file in the backend directory:

\`\`\`env
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=d2c_analytics

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis (for Celery)
REDIS_URL=redis://localhost:6379

# Google Cloud (for BigQuery)
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
GOOGLE_CLOUD_PROJECT=your-project-id
BIGQUERY_DATASET=d2c_analytics

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
\`\`\`

### 4. Start Backend Services with Docker

\`\`\`bash
# From the backend directory
docker-compose up -d

# This will start:
# - MongoDB database
# - Redis for caching
# - FastAPI application
# - Celery worker for background tasks
\`\`\`

### 5. Frontend Setup

\`\`\`bash
# Navigate to root directory
cd ..

# Install dependencies
npm install

# Create Next.js environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start the development server
npm run dev
\`\`\`

## Running the Application

### Start Backend (if not using Docker)

\`\`\`bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
\`\`\`

### Start Frontend

\`\`\`bash
npm run dev
\`\`\`

### Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## API Integration Setup

### 1. Shopify Integration

1. Go to your Shopify admin panel
2. Navigate to Apps > Manage private apps
3. Create a new private app
4. Enable the following permissions:
   - Read orders
   - Read products
   - Read customers
   - Read analytics
5. Copy the API key and shop domain

### 2. Facebook Ads Integration

1. Go to Facebook Developers Console
2. Create a new app
3. Add Marketing API product
4. Generate access token with ads_read permissions
5. Copy the access token

### 3. Google Ads Integration

1. Go to Google Ads API Console
2. Create a new project
3. Enable Google Ads API
4. Create credentials (OAuth 2.0)
5. Get developer token from Google Ads account
6. Copy access token, customer ID, and developer token

### 4. Shiprocket Integration

1. Login to Shiprocket dashboard
2. Go to Settings > API
3. Generate API key
4. Copy the API key

## Database Setup

### MongoDB Collections

The application will automatically create the following collections:

- `users` - User accounts and authentication
- `integrations` - Platform integration configurations
- `analytics_data` - Cached analytics data
- `sync_logs` - Data synchronization logs

### BigQuery Setup (Optional)

1. Create a Google Cloud Project
2. Enable BigQuery API
3. Create a service account
4. Download service account key JSON
5. Create BigQuery dataset named `d2c_analytics`

## Troubleshooting

### Common Issues

1. **Port conflicts**: Make sure ports 3000, 8000, 27017, and 6379 are available
2. **Docker issues**: Run `docker-compose down` and `docker-compose up -d` to restart
3. **Permission errors**: Make sure your user has Docker permissions
4. **API connection failures**: Check your API keys and network connectivity

### Logs

\`\`\`bash
# Backend logs
docker-compose logs api

# Database logs
docker-compose logs mongo

# Worker logs
docker-compose logs worker
\`\`\`

### Reset Database

\`\`\`bash
# Stop services
docker-compose down

# Remove volumes
docker-compose down -v

# Restart
docker-compose up -d
\`\`\`

## Production Deployment

### Environment Variables

Update production environment variables:

\`\`\`env
SECRET_KEY=generate-a-strong-secret-key
MONGODB_URL=mongodb://your-production-mongodb
ALLOWED_ORIGINS=https://yourdomain.com
\`\`\`

### SSL/HTTPS

1. Set up reverse proxy (Nginx)
2. Configure SSL certificates
3. Update CORS origins

### Monitoring

1. Set up application monitoring
2. Configure log aggregation
3. Set up health checks

## Scaling

### Horizontal Scaling

1. Use Docker Swarm or Kubernetes
2. Scale API and worker services
3. Use MongoDB replica sets
4. Implement Redis clustering

### Performance Optimization

1. Enable database indexing
2. Implement caching strategies
3. Use CDN for static assets
4. Optimize API queries

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review application logs
3. Check API documentation at `/docs`
4. Create an issue in the repository

## Security Considerations

1. Change default passwords
2. Use strong secret keys
3. Enable firewall rules
4. Regular security updates
5. API rate limiting
6. Input validation
