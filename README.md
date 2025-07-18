# D2C Analytics Platform - Simple Setup

## 🚀 Quick Setup (2 Steps)

### Step 1: Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
docker compose up -d
```

Your backend will be running at:
- **API**: http://82.29.164.244:8000
- **Docs**: http://82.29.164.244:8000/docs
- **MongoDB**: http://82.29.164.244:27017
- **Redis**: http://82.29.164.244:6379

### Step 2: Frontend Setup
```bash
npm install
npm run dev
```

Your frontend will be running at:
- **App**: http://82.29.164.244:3000

## 🎯 What You Get

### Dashboard Features
- **Toggle Demo/Live Data** - Switch between mock data and real platform data
- **Platform Connections** - Connect Shopify, Meta Ads, Google Ads, Shiprocket
- **AI Assistant** - Ask questions about your data
- **Comprehensive Analytics** - 50+ KPIs, charts, reports
- **Export Reports** - Download P&L and analytics reports

### Platform Integrations
From the **Credentials** page (`/credentials`), you can connect:

1. **Shopify**
   - Store domain
   - Access token

2. **Meta Ads (Facebook)**
   - Access token
   - Ad account ID

3. **Google Ads**
   - Developer token
   - Customer ID

4. **Shiprocket**
   - API key
   - Email

### AI Assistant
Ask questions like:
- "What's my best performing product?"
- "How can I improve my ROAS?"
- "Show me customer acquisition trends"
- "Generate a SQL query for revenue analysis"

## 🔧 Environment Setup

Create `.env.local` file:
```bash
# Required for AI features
GEMINI_API_KEY=your_gemini_api_key_here

# Backend connection (already configured)
NEXT_PUBLIC_API_URL=http://82.29.164.244:8000
NEXT_PUBLIC_APP_URL=http://82.29.164.244:3000
```

## 📊 How It Works

1. **Demo Mode**: Uses mock data for testing
2. **Live Mode**: Connects to your real platform APIs
3. **Backend Pipeline**: Processes and stores data from all platforms
4. **Frontend Dashboard**: Displays unified analytics
5. **AI Integration**: Provides insights and recommendations

## 🎉 That's It!

Your complete D2C analytics platform is ready with:
- ✅ Multi-platform data integration
- ✅ AI-powered insights
- ✅ Comprehensive dashboard
- ✅ Real-time analytics
- ✅ Export capabilities

Access your dashboard at http://82.29.164.244:3000