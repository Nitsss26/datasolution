# D2C Analytics SaaS - All-in-One Data Solution

A comprehensive full-stack SaaS solution for D2C businesses to track and analyze data from multiple platforms including Shopify, Facebook Ads, Google Ads, and Shiprocket.

## 🚀 Features

- **Multi-Platform Integration**: Connect Shopify, Facebook Ads, Google Ads, and Shiprocket
- **Beautiful Dashboard**: Real-time analytics with colorful charts and metrics
- **Time-based Filtering**: 7, 15, 30, and 90-day data views
- **Profit & Loss Reports**: Comprehensive P&L analysis
- **Scalable Architecture**: Built to easily add more platforms
- **Docker Support**: Easy deployment with Docker containers
- **Modern UI/UX**: Built with Next.js and Tailwind CSS

## 📋 Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Docker and Docker Compose**
- **MongoDB** (or use Docker)
- **Google Cloud Account** (for BigQuery)

## 🛠️ Installation & Setup

### 1. Clone the Repository

\`\`\`bash
git clone <repository-url>
cd d2c-analytics-saas
\`\`\`

### 2. Backend Setup

\`\`\`bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
\`\`\`

### 3. Environment Configuration

Edit `backend/.env` with your credentials:

\`\`\`env
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=d2c_analytics

# Security
SECRET_KEY=your-super-secret-key-here

# Google Cloud (for BigQuery)
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Redis (optional)
REDIS_URL=redis://localhost:6379
\`\`\`

### 4. Frontend Setup

\`\`\`bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
\`\`\`

### 5. Docker Setup (Recommended)

\`\`\`bash
# From the backend directory
cd backend

# Build and run with Docker Compose
docker-compose up --build

# This will start:
# - FastAPI backend on port 8000
# - MongoDB on port 27017
# - Redis on port 6379
\`\`\`

### 6. Manual Setup (Alternative)

If you prefer running without Docker:

\`\`\`bash
# Start MongoDB (install separately)
mongod

# Start Redis (install separately)
redis-server

# Start backend
cd backend
python -m uvicorn main:app --reload

# Start frontend (in new terminal)
cd frontend
npm run dev
\`\`\`

## 🔧 Platform Integration Setup

### Shopify Integration

1. **Create Private App**:
   - Go to your Shopify admin panel
   - Navigate to Apps > App and sales channel settings
   - Click "Develop apps for your store"
   - Create a new app with Admin API access

2. **Required Permissions**:
   - `read_orders`
   - `read_products`
   - `read_customers`
   - `read_analytics`

3. **Get Credentials**:
   - Shop URL: `your-store-name.myshopify.com`
   - Access Token: From the app's Admin API access tokens

### Facebook Ads Integration

1. **Create Facebook App**:
   - Go to [Facebook Developers](https://developers.facebook.com/)
   - Create a new app for Business use case
   - Add Marketing API product

2. **Get Access Token**:
   - Use Graph API Explorer to generate long-lived token
   - Required permissions: `ads_read`, `ads_management`

3. **Find Ad Account ID**:
   - Go to Facebook Ads Manager
   - Account ID is in the URL: `act_XXXXXXXXX`

### Google Ads Integration

1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project
   - Enable Google Ads API

2. **Get Credentials**:
   - Create OAuth 2.0 credentials
   - Generate refresh token using OAuth playground
   - Get developer token from Google Ads account

3. **Required Information**:
   - Customer ID (from Google Ads account)
   - Developer Token
   - OAuth Access Token

### Shiprocket Integration

1. **Get API Credentials**:
   - Login to Shiprocket panel
   - Go to API section
   - Use your login email and password

2. **API Documentation**:
   - [Shiprocket API Docs](https://apidocs.shiprocket.in/)

## 📊 Usage

### 1. User Registration

- Visit `http://localhost:3000`
- Create an account with your company details
- Login to access the dashboard

### 2. Connect Platforms

- Go to Integrations page
- Click "Connect" on desired platforms
- Enter your API credentials
- Test the connection

### 3. Sync Data

- After connecting, click "Sync Data"
- Data will be processed and stored
- View analytics on the dashboard

### 4. View Analytics

- **Dashboard**: Overview of all metrics
- **Charts**: Revenue trends, platform performance
- **Filters**: Select time ranges and platforms
- **Reports**: Generate P&L reports

## 🏗️ Architecture

\`\`\`
Frontend (Next.js) → Backend (FastAPI) → MongoDB + BigQuery
                ↓
         Platform APIs (Shopify, Facebook, Google, Shiprocket)
\`\`\`

### Key Components:

- **Frontend**: Next.js with Tailwind CSS for UI
- **Backend**: FastAPI with async support
- **Database**: MongoDB for user data and analytics
- **Analytics**: BigQuery for data warehousing
- **Caching**: Redis for performance
- **Charts**: Recharts for data visualization

## 🔄 Data Flow

1. **User Authentication**: JWT-based auth system
2. **Platform Connection**: Store encrypted credentials
3. **Data Sync**: Scheduled jobs fetch data from APIs
4. **Data Processing**: Clean and transform data
5. **Analytics**: Calculate metrics and KPIs
6. **Visualization**: Display charts and reports

## 📈 Metrics Tracked

### Revenue Metrics
- Total Revenue
- Average Order Value (AOV)
- Revenue per Channel
- Gross Merchandise Value (GMV)

### Cost Metrics
- Cost of Goods Sold (COGS)
- Ad Spend
- Marketplace Fees
- Shipping Costs
- Customer Acquisition Cost (CAC)

### Profit Metrics
- Gross Profit
- Net Profit
- Gross Margin
- Net Margin

### Marketing Metrics
- Return on Ad Spend (ROAS)
- Click-Through Rate (CTR)
- Conversion Rate
- Cost per Click (CPC)

## 🚀 Deployment

### Production Deployment

1. **Backend Deployment**:
   \`\`\`bash
   # Build Docker image
   docker build -t d2c-analytics-backend .
   
   # Run container
   docker run -d -p 8000:8000 d2c-analytics-backend
   \`\`\`

2. **Frontend Deployment**:
   \`\`\`bash
   # Build for production
   npm run build
   
   # Start production server
   npm start
   \`\`\`

### Environment Variables for Production

\`\`\`env
# Backend
MONGODB_URL=mongodb://production-mongo:27017
SECRET_KEY=your-production-secret-key
GOOGLE_CLOUD_PROJECT=production-project-id

# Frontend
NEXT_PUBLIC_API_URL=https://your-api-domain.com
\`\`\`

## 🔍 Troubleshooting

### Common Issues

1. **Connection Failed**:
   - Check API credentials
   - Verify API permissions
   - Check rate limits

2. **Data Not Syncing**:
   - Check logs in backend
   - Verify MongoDB connection
   - Check API rate limits

3. **Charts Not Loading**:
   - Check browser console for errors
   - Verify API endpoints are accessible
   - Check data format in responses

### Debug Commands

\`\`\`bash
# Check backend logs
docker-compose logs app

# Check MongoDB connection
docker-compose exec mongo mongo

# Check API endpoints
curl http://localhost:8000/health
\`\`\`

## 📝 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🛡️ Security

- JWT-based authentication
- Password hashing with bcrypt
- API rate limiting
- Input validation
- CORS protection
- Encrypted credential storage

## 🎯 Future Enhancements

- Add more platforms (Amazon, Flipkart, Zepto)
- Real-time data streaming
- Advanced analytics and predictions
- Mobile app
- Multi-tenant support
- Advanced reporting features

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check logs for error messages
4. Create an issue in the repository

## 📄 License

This project is licensed under the MIT License.
\`\`\`

This comprehensive D2C Analytics SaaS solution includes:

1. **Backend** (Python FastAPI):
   - User authentication system
   - Platform integrations (Shopify, Facebook Ads, Google Ads, Shiprocket)
   - Analytics processing
   - BigQuery integration
   - Docker support

2. **Frontend** (Next.js):
   - Beautiful dashboard with charts
   - User authentication
   - Platform management
   - Time-based filtering
   - Responsive design

3. **Key Features**:
   - Multi-platform data integration
   - Real-time analytics
   - Profit & Loss reports
   - Scalable architecture
   - Docker environment
   - Beautiful UI/UX

The solution is designed to be easily scalable for additional platforms like Amazon, Flipkart, and Zepto as requested. The architecture separates concerns properly with a Python backend for data processing and a modern React frontend for visualization.

To get started:
1. Run `docker-compose up --build` in the backend directory
2. Run `npm install && npm run dev` in the frontend directory
3. Visit `http://localhost:3000` to access the application
