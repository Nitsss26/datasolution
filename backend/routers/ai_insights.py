from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

from database import save_ai_query, get_recent_ai_queries

logger = logging.getLogger(__name__)

router = APIRouter()

class AIQueryRequest(BaseModel):
    query: str
    data: Optional[Dict[str, Any]] = None
    user_id: str = "default"

class AIQueryResponse(BaseModel):
    response: str
    sql_query: Optional[str] = None
    insights: Optional[List[Dict[str, Any]]] = None
    timestamp: str

@router.post("/query", response_model=AIQueryResponse)
async def process_ai_query(request: AIQueryRequest):
    """Process AI query and return insights"""
    try:
        logger.info(f"AI Query: {request.query[:100]}...")
        
        # Generate AI response based on query and data
        ai_response = await generate_ai_response(request.query, request.data)
        
        # Save query for analytics
        await save_ai_query(
            user_id=request.user_id,
            query=request.query,
            response=ai_response["response"],
            sql_query=ai_response.get("sql_query")
        )
        
        return AIQueryResponse(
            response=ai_response["response"],
            sql_query=ai_response.get("sql_query"),
            insights=ai_response.get("insights", []),
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"AI query processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"AI query failed: {str(e)}")

async def generate_ai_response(query: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate AI response based on query and data"""
    try:
        # Analyze query intent
        query_lower = query.lower()
        
        # Revenue-related queries
        if any(word in query_lower for word in ["revenue", "sales", "income", "earning"]):
            return await handle_revenue_query(query, data)
        
        # Cost-related queries
        elif any(word in query_lower for word in ["cost", "expense", "spend", "budget"]):
            return await handle_cost_query(query, data)
        
        # Profit-related queries
        elif any(word in query_lower for word in ["profit", "margin", "roi", "roas"]):
            return await handle_profit_query(query, data)
        
        # Customer-related queries
        elif any(word in query_lower for word in ["customer", "user", "buyer", "retention"]):
            return await handle_customer_query(query, data)
        
        # Marketing-related queries
        elif any(word in query_lower for word in ["ad", "campaign", "marketing", "conversion"]):
            return await handle_marketing_query(query, data)
        
        # Delivery-related queries
        elif any(word in query_lower for word in ["delivery", "shipping", "logistics", "courier"]):
            return await handle_delivery_query(query, data)
        
        # General business queries
        else:
            return await handle_general_query(query, data)
            
    except Exception as e:
        logger.error(f"AI response generation failed: {e}")
        return {
            "response": "I apologize, but I'm having trouble processing your query right now. Please try rephrasing your question or contact support.",
            "sql_query": None,
            "insights": []
        }

async def handle_revenue_query(query: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle revenue-related queries"""
    if not data:
        return {
            "response": """📊 **Revenue Analysis**

Based on typical D2C patterns in India:

💰 **Current Revenue Insights:**
- Your total revenue appears to be performing well
- Average Order Value (AOV) in Indian D2C typically ranges from ₹1,500-₹4,000
- Revenue growth of 15-25% month-over-month is considered healthy

🎯 **Revenue Optimization Tips:**
1. **Increase AOV**: Bundle products, offer free shipping above ₹999
2. **Festival Campaigns**: Leverage Diwali, Dussehra for 40-60% revenue boost
3. **Regional Targeting**: Focus on Tier-1 cities for higher AOV
4. **Payment Options**: COD increases conversion by 20-30% in India

📈 **Key Metrics to Track:**
- Monthly Recurring Revenue (MRR)
- Revenue per Customer
- Seasonal Revenue Patterns
- Channel-wise Revenue Distribution

Would you like me to analyze specific revenue metrics from your data?""",
            "sql_query": "SELECT DATE(created_at) as date, SUM(total_price) as daily_revenue FROM shopify_orders WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) GROUP BY DATE(created_at) ORDER BY date;",
            "insights": [
                {"type": "opportunity", "title": "AOV Optimization", "description": "Consider bundling to increase average order value", "impact": "high"},
                {"type": "seasonal", "title": "Festival Planning", "description": "Prepare for upcoming festival seasons", "impact": "high"}
            ]
        }
    
    # Analyze actual data if provided
    d2c_metrics = data.get("d2cMetrics", {})
    total_revenue = d2c_metrics.get("totalRevenue", 0)
    aov = d2c_metrics.get("averageOrderValue", 0)
    
    return {
        "response": f"""📊 **Your Revenue Analysis**

💰 **Current Performance:**
- Total Revenue: ₹{total_revenue:,.2f}
- Average Order Value: ₹{aov:,.2f}
- Revenue Growth: {"Strong" if total_revenue > 500000 else "Moderate" if total_revenue > 100000 else "Growing"}

🎯 **Insights:**
- Your AOV of ₹{aov:,.2f} is {"above" if aov > 2500 else "below"} the Indian D2C average
- {"Excellent performance! Focus on scaling." if total_revenue > 1000000 else "Good foundation. Consider growth strategies."}

📈 **Recommendations:**
1. {"Maintain current strategy and scale" if aov > 3000 else "Implement upselling to increase AOV"}
2. {"Expand to new markets" if total_revenue > 500000 else "Focus on customer retention"}
3. Leverage seasonal campaigns for revenue boost

Would you like specific strategies for your revenue segment?""",
        "sql_query": "SELECT DATE(created_at) as date, SUM(total_price) as revenue, COUNT(*) as orders, AVG(total_price) as aov FROM shopify_orders WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) GROUP BY DATE(created_at) ORDER BY date;",
        "insights": [
            {"type": "performance", "title": f"Revenue: ₹{total_revenue:,.0f}", "description": "Current revenue performance", "impact": "info"},
            {"type": "optimization", "title": f"AOV: ₹{aov:,.0f}", "description": "Average order value analysis", "impact": "medium"}
        ]
    }

async def handle_cost_query(query: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle cost-related queries"""
    return {
        "response": """💸 **Cost Analysis & Optimization**

🔍 **Major Cost Categories in D2C:**

1. **Customer Acquisition Cost (CAC)**: ₹800-₹2,000
2. **Cost of Goods Sold (COGS)**: 40-60% of revenue
3. **Shipping Costs**: ₹50-₹150 per order
4. **Payment Gateway**: 2-3% of transaction value
5. **Marketing Spend**: 15-25% of revenue

💡 **Cost Optimization Strategies:**
- **Shipping**: Negotiate better rates, optimize packaging
- **CAC**: Focus on organic channels, improve retention
- **COGS**: Bulk purchasing, supplier negotiations
- **Returns**: Improve product descriptions, sizing guides

📊 **Benchmarks for India:**
- Total costs should be <70% of revenue for profitability
- Shipping costs: Keep under 8% of AOV
- Marketing spend: 20% of revenue is optimal

Would you like me to analyze your specific cost structure?""",
        "sql_query": "SELECT 'COGS' as cost_type, SUM(cost_of_goods) as amount FROM orders UNION ALL SELECT 'Shipping', SUM(shipping_cost) FROM orders UNION ALL SELECT 'Marketing', SUM(ad_spend) FROM campaigns;",
        "insights": [
            {"type": "optimization", "title": "Cost Structure Review", "description": "Analyze major cost components", "impact": "high"},
            {"type": "benchmark", "title": "Industry Comparison", "description": "Compare with D2C benchmarks", "impact": "medium"}
        ]
    }

async def handle_profit_query(query: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle profit-related queries"""
    if data:
        d2c_metrics = data.get("d2cMetrics", {})
        gross_profit = d2c_metrics.get("grossProfit", 0)
        net_profit = d2c_metrics.get("netProfit", 0)
        gross_margin = d2c_metrics.get("grossMargin", 0)
        net_margin = d2c_metrics.get("netMargin", 0)
        
        return {
            "response": f"""📈 **Your Profit Analysis**

💰 **Current Profitability:**
- Gross Profit: ₹{gross_profit:,.2f}
- Net Profit: ₹{net_profit:,.2f}
- Gross Margin: {gross_margin:.1f}%
- Net Margin: {net_margin:.1f}%

🎯 **Performance Assessment:**
- Gross Margin: {"Excellent" if gross_margin > 60 else "Good" if gross_margin > 45 else "Needs Improvement"}
- Net Margin: {"Strong" if net_margin > 20 else "Moderate" if net_margin > 10 else "Focus Required"}

📊 **Improvement Strategies:**
1. {"Maintain current efficiency" if net_margin > 20 else "Reduce operational costs"}
2. {"Scale current model" if gross_margin > 50 else "Optimize product mix"}
3. {"Expand market reach" if net_profit > 100000 else "Focus on unit economics"}

🚀 **Next Steps:**
- {"Ready for aggressive scaling" if net_margin > 15 else "Optimize before scaling"}
- Focus on high-margin products
- Implement cost control measures""",
            "sql_query": "SELECT (SUM(revenue) - SUM(cogs)) as gross_profit, (SUM(revenue) - SUM(total_costs)) as net_profit, ((SUM(revenue) - SUM(cogs))/SUM(revenue))*100 as gross_margin FROM financial_data WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY);",
            "insights": [
                {"type": "performance", "title": f"Net Margin: {net_margin:.1f}%", "description": "Current profitability level", "impact": "high"},
                {"type": "benchmark", "title": "Margin Analysis", "description": "Compare with industry standards", "impact": "medium"}
            ]
        }
    
    return {
        "response": """📈 **Profit Optimization Guide**

🎯 **D2C Profit Benchmarks (India):**
- Gross Margin: 50-70% (target)
- Net Margin: 15-25% (healthy)
- EBITDA Margin: 20-30% (good)

💡 **Profit Improvement Strategies:**

**1. Increase Gross Margin:**
- Optimize product pricing
- Reduce COGS through bulk purchasing
- Focus on high-margin products

**2. Improve Net Margin:**
- Reduce customer acquisition costs
- Optimize operational efficiency
- Automate repetitive processes

**3. Scale Profitably:**
- Maintain unit economics while growing
- Focus on lifetime value over acquisition
- Implement data-driven decisions

📊 **Key Metrics to Monitor:**
- Contribution Margin per Order
- Customer Lifetime Value (CLV)
- Payback Period for CAC

Would you like me to analyze your specific profit metrics?""",
        "insights": [
            {"type": "strategy", "title": "Margin Optimization", "description": "Focus on high-margin products", "impact": "high"},
            {"type": "efficiency", "title": "Cost Control", "description": "Implement systematic cost reduction", "impact": "medium"}
        ]
    }

async def handle_customer_query(query: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle customer-related queries"""
    return {
        "response": """👥 **Customer Analytics & Insights**

🔍 **Key Customer Metrics:**

**Acquisition:**
- Customer Acquisition Cost (CAC): ₹800-₹2,000
- Conversion Rate: 2-4% (industry average)
- Traffic to Customer: 1-3%

**Retention:**
- Repeat Purchase Rate: 20-40%
- Customer Lifetime Value: ₹3,000-₹15,000
- Churn Rate: 5-15% monthly

**Engagement:**
- Average Session Duration: 2-4 minutes
- Pages per Session: 3-5 pages
- Email Open Rate: 15-25%

💡 **Customer Optimization Strategies:**

**1. Improve Acquisition:**
- Focus on high-intent keywords
- Optimize landing pages
- Use social proof and reviews

**2. Increase Retention:**
- Implement loyalty programs
- Personalized email campaigns
- Post-purchase engagement

**3. Boost Lifetime Value:**
- Cross-sell and upsell
- Subscription models
- Premium product tiers

🎯 **India-Specific Insights:**
- COD customers have 20% higher retention
- Regional language content improves engagement
- Festival season drives 40% of annual purchases

Would you like specific customer segment analysis?""",
        "sql_query": "SELECT COUNT(DISTINCT customer_id) as total_customers, AVG(total_spent) as avg_clv, COUNT(*)/COUNT(DISTINCT customer_id) as avg_orders_per_customer FROM customers JOIN orders ON customers.id = orders.customer_id;",
        "insights": [
            {"type": "retention", "title": "Customer Loyalty", "description": "Implement retention strategies", "impact": "high"},
            {"type": "acquisition", "title": "CAC Optimization", "description": "Focus on cost-effective channels", "impact": "medium"}
        ]
    }

async def handle_marketing_query(query: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle marketing-related queries"""
    if data:
        ad_metrics = data.get("adMetrics", {})
        roas = ad_metrics.get("returnOnAdSpend", 0)
        ctr = ad_metrics.get("clickThroughRate", 0)
        conversion_rate = ad_metrics.get("conversionRate", 0)
        
        return {
            "response": f"""🎯 **Your Marketing Performance**

📊 **Current Metrics:**
- ROAS: {roas:.1f}x
- Click-Through Rate: {ctr:.2f}%
- Conversion Rate: {conversion_rate:.2f}%

🚀 **Performance Assessment:**
- ROAS: {"Excellent" if roas > 4 else "Good" if roas > 3 else "Needs Improvement"}
- CTR: {"Above Average" if ctr > 2 else "Average" if ctr > 1 else "Below Average"}
- Conversion: {"Strong" if conversion_rate > 3 else "Moderate" if conversion_rate > 2 else "Focus Required"}

💡 **Optimization Recommendations:**
1. {"Scale winning campaigns" if roas > 4 else "Optimize targeting and creatives"}
2. {"Expand to new audiences" if ctr > 2 else "Improve ad copy and visuals"}
3. {"Increase budget allocation" if conversion_rate > 3 else "Optimize landing pages"}

🎯 **Next Actions:**
- {"Ready for aggressive scaling" if roas > 4 and conversion_rate > 3 else "Focus on optimization first"}
- A/B test different creatives and audiences
- Implement retargeting campaigns""",
            "sql_query": "SELECT campaign_name, SUM(spend) as total_spend, SUM(conversions) as total_conversions, (SUM(conversion_value)/SUM(spend)) as roas FROM ad_campaigns WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) GROUP BY campaign_name ORDER BY roas DESC;",
            "insights": [
                {"type": "performance", "title": f"ROAS: {roas:.1f}x", "description": "Return on ad spend analysis", "impact": "high"},
                {"type": "optimization", "title": "Campaign Performance", "description": "Identify top performing campaigns", "impact": "medium"}
            ]
        }
    
    return {
        "response": """🎯 **Marketing Analytics & Optimization**

📊 **Key Marketing Metrics:**

**Performance Indicators:**
- ROAS: 4-6x (target for profitability)
- CTR: 1.5-3% (industry benchmark)
- Conversion Rate: 2-5% (e-commerce average)
- CPC: ₹15-₹50 (varies by industry)

**Channel Performance (India):**
- Facebook Ads: High reach, good for awareness
- Google Ads: High intent, better conversion
- Instagram: Strong for lifestyle brands
- YouTube: Effective for product demos

💡 **Optimization Strategies:**

**1. Campaign Structure:**
- Separate campaigns by product categories
- Use audience segmentation
- Implement dayparting

**2. Creative Optimization:**
- Test multiple ad formats
- Use local language content
- Include social proof and reviews

**3. Targeting Refinement:**
- Focus on high-value audiences
- Use lookalike audiences
- Implement retargeting funnels

🇮🇳 **India-Specific Tips:**
- Festival season campaigns (Diwali, Dussehra)
- Regional targeting for better relevance
- Mobile-first creative approach (70% mobile traffic)

Would you like campaign-specific recommendations?""",
        "insights": [
            {"type": "strategy", "title": "Channel Optimization", "description": "Focus on high-performing channels", "impact": "high"},
            {"type": "creative", "title": "Ad Creative Testing", "description": "Implement systematic A/B testing", "impact": "medium"}
        ]
    }

async def handle_delivery_query(query: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle delivery-related queries"""
    return {
        "response": """🚚 **Delivery & Logistics Optimization**

📦 **Key Delivery Metrics:**

**Performance Indicators:**
- Average Delivery Time: 2-4 days (metro cities)
- On-Time Delivery: 85-95% (target)
- Shipping Cost: ₹50-₹150 per order
- Return Rate: 5-15% (category dependent)

**Cost Breakdown:**
- Forward Shipping: ₹40-₹120
- COD Charges: ₹15-₹25
- Return Shipping: ₹30-₹80
- Packaging: ₹10-₹30

💡 **Optimization Strategies:**

**1. Cost Reduction:**
- Negotiate volume discounts with couriers
- Optimize packaging dimensions
- Implement zone-wise shipping rates

**2. Speed Improvement:**
- Use multiple courier partners
- Implement same-day delivery in metros
- Optimize warehouse locations

**3. Customer Experience:**
- Provide real-time tracking
- Send proactive delivery updates
- Offer flexible delivery options

🇮🇳 **India-Specific Insights:**
- COD orders have 20% higher delivery costs
- Tier-2/3 cities take 1-2 extra days
- Festival seasons see 30% delivery delays
- Regional courier partners perform better in local areas

📊 **Benchmarks:**
- Shipping cost should be <8% of AOV
- On-time delivery >90% for customer satisfaction
- Return rate <10% indicates good product-market fit

Would you like specific courier performance analysis?""",
        "sql_query": "SELECT courier_name, AVG(delivery_time) as avg_delivery_days, (COUNT(CASE WHEN status='delivered' THEN 1 END)/COUNT(*))*100 as delivery_success_rate, AVG(shipping_cost) as avg_cost FROM shipments WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) GROUP BY courier_name;",
        "insights": [
            {"type": "cost", "title": "Shipping Optimization", "description": "Reduce shipping costs through negotiation", "impact": "high"},
            {"type": "experience", "title": "Delivery Speed", "description": "Improve delivery times for better CX", "impact": "medium"}
        ]
    }

async def handle_general_query(query: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle general business queries"""
    return {
        "response": f"""🚀 **D2C Business Intelligence**

Based on your query: "{query}"

📊 **Comprehensive Business Overview:**

**Revenue Health:**
- Focus on sustainable growth (15-25% MoM)
- Maintain healthy unit economics
- Diversify revenue streams

**Cost Management:**
- Keep total costs <70% of revenue
- Optimize customer acquisition costs
- Monitor operational efficiency

**Customer Success:**
- Improve lifetime value through retention
- Reduce churn with better experience
- Implement loyalty programs

**Market Expansion:**
- Leverage seasonal opportunities
- Explore new customer segments
- Consider geographic expansion

💡 **Key Performance Indicators:**
- Revenue Growth Rate
- Customer Acquisition Cost (CAC)
- Customer Lifetime Value (CLV)
- Gross & Net Margins
- Inventory Turnover

🇮🇳 **India D2C Landscape:**
- Mobile-first approach (70% traffic)
- COD remains important (40% orders)
- Festival seasons drive 50% annual sales
- Tier-2/3 cities showing rapid growth

Would you like me to dive deeper into any specific area of your business?""",
        "insights": [
            {"type": "overview", "title": "Business Health Check", "description": "Comprehensive performance review", "impact": "high"},
            {"type": "strategy", "title": "Growth Opportunities", "description": "Identify expansion possibilities", "impact": "medium"}
        ]
    }

@router.get("/history/{user_id}")
async def get_ai_query_history(user_id: str, limit: int = 10):
    """Get recent AI query history for a user"""
    try:
        queries = await get_recent_ai_queries(user_id, limit)
        
        return {
            "user_id": user_id,
            "queries": queries,
            "count": len(queries)
        }
        
    except Exception as e:
        logger.error(f"Get query history failed: {e}")
        raise HTTPException(status_code=500, detail=f"Get history failed: {str(e)}")

@router.get("/insights/generate")
async def generate_business_insights(data: Optional[Dict[str, Any]] = None):
    """Generate automated business insights"""
    try:
        insights = []
        
        if data:
            d2c_metrics = data.get("d2cMetrics", {})
            ad_metrics = data.get("adMetrics", {})
            
            # Revenue insights
            total_revenue = d2c_metrics.get("totalRevenue", 0)
            if total_revenue > 1000000:
                insights.append({
                    "type": "success",
                    "title": "Strong Revenue Performance",
                    "description": f"Your revenue of ₹{total_revenue:,.0f} indicates strong market traction",
                    "priority": "high"
                })
            
            # ROAS insights
            roas = ad_metrics.get("returnOnAdSpend", 0)
            if roas > 4:
                insights.append({
                    "type": "opportunity",
                    "title": "Scale Marketing Spend",
                    "description": f"With ROAS of {roas:.1f}x, consider increasing ad budget",
                    "priority": "high"
                })
            elif roas < 3:
                insights.append({
                    "type": "warning",
                    "title": "Optimize Ad Performance",
                    "description": f"ROAS of {roas:.1f}x is below optimal. Review targeting and creatives",
                    "priority": "high"
                })
        
        # Default insights
        if not insights:
            insights = [
                {
                    "type": "info",
                    "title": "Data Connection Required",
                    "description": "Connect your platforms to get personalized insights",
                    "priority": "medium"
                },
                {
                    "type": "tip",
                    "title": "Festival Season Preparation",
                    "description": "Plan campaigns for upcoming festival seasons in India",
                    "priority": "medium"
                }
            ]
        
        return {
            "insights": insights,
            "generated_at": datetime.utcnow().isoformat(),
            "currency": "INR"
        }
        
    except Exception as e:
        logger.error(f"Generate insights failed: {e}")
        raise HTTPException(status_code=500, detail=f"Generate insights failed: {str(e)}")