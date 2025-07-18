# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
npm install
```

### 2. Set Up Environment
Create `.env.local` file in the root directory:
```bash
# Required for AI Assistant
GEMINI_API_KEY=your_gemini_api_key_here

# Optional - for future integrations
SHOPIFY_API_KEY=your_shopify_key
FACEBOOK_ACCESS_TOKEN=your_facebook_token
GOOGLE_ADS_DEVELOPER_TOKEN=your_google_ads_token
SHIPROCKET_API_KEY=your_shiprocket_key
```

### 3. Start the Application
```bash
npm run dev
```

Visit http://localhost:3000 to see the application!

## 🔑 Getting a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env.local` file

## 📱 Available Pages

- **Home**: http://localhost:3000 - Landing page
- **Dashboard**: http://localhost:3000/dashboard - Main analytics dashboard
- **AI Assistant**: http://localhost:3000/ai-assistant - Chat with AI about your data
- **Credentials**: http://localhost:3000/credentials - Configure platform integrations

## 🎯 Try These Features

### Dashboard
- View comprehensive D2C metrics
- Switch between different time ranges
- Explore platform-specific data
- Customize charts and themes

### AI Assistant
Try asking questions like:
- "What's my best performing product category?"
- "How can I improve my conversion rate?"
- "Show me trends in customer acquisition cost"
- "Generate a SQL query for monthly revenue"

### Credentials
- Configure Shopify, Facebook Ads, Google Ads, and Shiprocket
- Test connections (currently simulated)
- View connection status

## 🛠️ Development

### Project Structure
```
├── app/                 # Next.js app directory
│   ├── dashboard/       # Dashboard page
│   ├── ai-assistant/    # AI chat interface
│   ├── credentials/     # Platform configuration
│   └── api/            # API routes
├── components/         # Reusable components
├── hooks/             # Custom React hooks
├── lib/               # Utility functions
└── types/             # TypeScript definitions
```

### Key Files
- `app/dashboard/page.tsx` - Main dashboard
- `app/ai-assistant/page.tsx` - AI chat interface
- `hooks/use-ai.ts` - AI functionality
- `lib/gemini-ai.ts` - AI integration
- `types/analytics.ts` - Data type definitions

## 🔧 Troubleshooting

### Common Issues

**AI Assistant not working?**
- Check if GEMINI_API_KEY is set in `.env.local`
- Verify the API key is valid
- Check browser console for errors

**Dashboard not loading data?**
- The app uses demo data by default
- Check if the demo API route is working: http://localhost:3000/api/demo/analytics

**Styling issues?**
- Make sure Tailwind CSS is properly configured
- Check if all UI components are imported correctly

### Getting Help
- Check the browser console for error messages
- Verify all dependencies are installed
- Ensure you're using Node.js 18 or higher

## 🎉 You're Ready!

The application is now running with:
- ✅ Interactive dashboard with D2C metrics
- ✅ AI-powered assistant for business insights
- ✅ Platform integration setup
- ✅ Modern, responsive UI
- ✅ Dark/light theme support

Start exploring your D2C analytics platform!