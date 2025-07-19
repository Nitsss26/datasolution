#!/bin/bash

# D2C Analytics Platform - Comprehensive Startup Script
echo "🚀 Starting D2C Analytics Platform..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if required tools are installed
check_requirements() {
    print_header "🔍 Checking Requirements..."
    
    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_status "Node.js found: $NODE_VERSION"
    else
        print_error "Node.js is not installed. Please install Node.js 18+ first."
        exit 1
    fi
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_status "Python found: $PYTHON_VERSION"
    else
        print_error "Python 3 is not installed. Please install Python 3.8+ first."
        exit 1
    fi
    
    # Check Docker (optional)
    if command -v docker &> /dev/null; then
        print_status "Docker found"
    else
        print_warning "Docker not found. Some features may not work."
    fi
}

# Setup Frontend
setup_frontend() {
    print_header "🎨 Setting up Frontend..."
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    if [ $? -eq 0 ]; then
        print_status "Frontend dependencies installed successfully"
    else
        print_error "Failed to install frontend dependencies"
        exit 1
    fi
}

# Setup Backend
setup_backend() {
    print_header "🔧 Setting up Backend..."
    
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        print_status "Backend dependencies installed successfully"
    else
        print_error "Failed to install backend dependencies"
        exit 1
    fi
    
    cd ..
}

# Setup Environment Variables
setup_environment() {
    print_header "🔐 Setting up Environment Variables..."
    
    # Frontend environment
    if [ ! -f ".env.local" ]; then
        print_status "Creating frontend .env.local file..."
        cat > .env.local << EOL
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=D2C Analytics Pro
NEXT_PUBLIC_APP_VERSION=1.0.0
EOL
    fi
    
    # Backend environment
    if [ ! -f "backend/.env" ]; then
        print_status "Creating backend .env file..."
        cat > backend/.env << EOL
# Database Configuration
MONGODB_URL=mongodb://localhost:27017/d2c_analytics
DATABASE_NAME=d2c_analytics

# BigQuery Configuration (Optional - for production)
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
BIGQUERY_DATASET=d2c_analytics

# API Keys (Add your actual keys)
SHOPIFY_API_KEY=your-shopify-api-key
SHOPIFY_API_SECRET=your-shopify-api-secret
SHOPIFY_ACCESS_TOKEN=your-shopify-access-token
SHOPIFY_SHOP_DOMAIN=your-shop.myshopify.com

GOOGLE_ADS_DEVELOPER_TOKEN=your-google-ads-developer-token
GOOGLE_ADS_CLIENT_ID=your-google-ads-client-id
GOOGLE_ADS_CLIENT_SECRET=your-google-ads-client-secret
GOOGLE_ADS_REFRESH_TOKEN=your-google-ads-refresh-token
GOOGLE_ADS_CUSTOMER_ID=your-google-ads-customer-id

FACEBOOK_ACCESS_TOKEN=your-facebook-access-token
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
FACEBOOK_AD_ACCOUNT_ID=your-facebook-ad-account-id

SHIPROCKET_API_KEY=your-shiprocket-api-key
SHIPROCKET_EMAIL=your-shiprocket-email
SHIPROCKET_PASSWORD=your-shiprocket-password

# Security
JWT_SECRET=your-jwt-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here

# Email Configuration (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Redis Configuration (Optional)
REDIS_URL=redis://localhost:6379

# Environment
ENVIRONMENT=development
DEBUG=true
EOL
        print_warning "Please update backend/.env with your actual API keys and credentials"
    fi
}

# Start Services
start_services() {
    print_header "🚀 Starting Services..."
    
    # Start MongoDB (if using Docker)
    if command -v docker &> /dev/null; then
        print_status "Starting MongoDB with Docker..."
        docker run -d --name d2c-mongodb -p 27017:27017 mongo:latest
    else
        print_warning "Please ensure MongoDB is running on localhost:27017"
    fi
    
    # Start Redis (if using Docker)
    if command -v docker &> /dev/null; then
        print_status "Starting Redis with Docker..."
        docker run -d --name d2c-redis -p 6379:6379 redis:latest
    else
        print_warning "Redis is optional but recommended for caching"
    fi
    
    sleep 3
}

# Start Backend
start_backend() {
    print_header "🔧 Starting Backend Server..."
    
    cd backend
    source venv/bin/activate
    
    # Start FastAPI server in background
    print_status "Starting FastAPI server on http://localhost:8000"
    python main.py &
    BACKEND_PID=$!
    
    cd ..
    
    # Wait for backend to start
    sleep 5
    
    # Check if backend is running
    if curl -s http://localhost:8000/health > /dev/null; then
        print_status "Backend server started successfully"
    else
        print_error "Backend server failed to start"
        exit 1
    fi
}

# Start Frontend
start_frontend() {
    print_header "🎨 Starting Frontend Server..."
    
    print_status "Starting Next.js development server on http://localhost:3000"
    npm run dev &
    FRONTEND_PID=$!
    
    # Wait for frontend to start
    sleep 10
    
    # Check if frontend is running
    if curl -s http://localhost:3000 > /dev/null; then
        print_status "Frontend server started successfully"
    else
        print_error "Frontend server failed to start"
        exit 1
    fi
}

# Display final information
show_info() {
    print_header "✅ D2C Analytics Platform Started Successfully!"
    echo ""
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo "🔍 Health Check: http://localhost:8000/health"
    echo ""
    echo "📋 Available Features:"
    echo "  • Comprehensive Dashboard with Sidebar Navigation"
    echo "  • Data Warehouse (BigQuery Integration)"
    echo "  • Comprehensive Data Tables (Shopify, Google Ads, Meta Ads, Shiprocket)"
    echo "  • Advanced Charts and Visualizations"
    echo "  • AI Analytics Assistant"
    echo "  • Platform Connectors (Shopify, Google Ads, Meta Ads, Shiprocket)"
    echo "  • Export/Import Functionality"
    echo "  • Real-time Data Sync"
    echo ""
    echo "🔧 Next Steps:"
    echo "  1. Update backend/.env with your actual API credentials"
    echo "  2. Configure BigQuery for production data warehouse"
    echo "  3. Set up your platform integrations"
    echo "  4. Customize the dashboard layout"
    echo ""
    echo "📖 Documentation:"
    echo "  • README.md - General setup and usage"
    echo "  • QUICK_START.md - Quick start guide"
    echo "  • ULTIMATE_SETUP.md - Complete setup instructions"
    echo ""
    echo "🛑 To stop the servers:"
    echo "  Press Ctrl+C or run: pkill -f 'python main.py' && pkill -f 'next dev'"
    echo ""
}

# Cleanup function
cleanup() {
    print_header "🛑 Shutting down servers..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    pkill -f "python main.py" 2>/dev/null
    pkill -f "next dev" 2>/dev/null
    print_status "Servers stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    print_header "🚀 D2C Analytics Platform - Comprehensive Setup"
    echo ""
    
    check_requirements
    setup_frontend
    setup_backend
    setup_environment
    start_services
    start_backend
    start_frontend
    show_info
    
    # Keep script running
    print_status "Servers are running. Press Ctrl+C to stop."
    wait
}

# Run main function
main