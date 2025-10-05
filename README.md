# 🤖 Agent Saad - Customer Sentiment Alert System

An intelligent AI agent that monitors social media (Twitter/X and Reddit) for negative sentiment about your brand, automatically detects urgent issues, and sends real-time alerts via Slack and Email with recommended responses.

## 🌟 Features

- **Real-time Sentiment Analysis**: Uses state-of-the-art AI models (DistilBERT) to analyze customer sentiment
- **Multi-Platform Monitoring**: Monitors Twitter/X and Reddit for brand mentions
- **Smart Alert System**: Automatically prioritizes alerts by urgency (Critical, High, Medium, Low)
- **Intelligent Recommendations**: Provides context-aware response suggestions for each alert
- **Beautiful Dashboard**: Modern web interface to view and manage all alerts
- **Multiple Alert Channels**: Sends notifications via Slack and Email
- **Automated Monitoring**: Runs continuously with configurable check intervals
- **No Duplicate Alerts**: Smart tracking prevents duplicate notifications

## 📋 Prerequisites

- Python 3.8 or higher
- Twitter/X API credentials (Bearer Token)
- Reddit API credentials (Client ID & Secret)
- Slack Bot Token (optional)
- Email SMTP credentials (optional)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Edit the `.env` file with your credentials:

```bash
# Twitter/X API Credentials
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_SECRET=your_twitter_access_secret
TWITTER_BEARER_TOKEN=your_twitter_bearer_token

# Reddit API Credentials
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=Agent-Saad/1.0

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
ALERT_EMAIL_TO=support@yourcompany.com

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_CHANNEL=#alerts

# Monitoring Configuration
KEYWORDS=your_brand,your_product,your_company
CHECK_INTERVAL_MINUTES=15
SENTIMENT_THRESHOLD=-0.3
```

### 3. Run the Application

```bash
python run.py
```

The dashboard will be available at: **http://localhost:5000**

## 🎯 How It Works

1. **Monitoring**: Agent Saad continuously monitors Twitter and Reddit for mentions of your keywords
2. **Analysis**: Each mention is analyzed using AI sentiment analysis (DistilBERT model)
3. **Filtering**: Only negative sentiment below your threshold triggers an alert
4. **Prioritization**: Alerts are classified by urgency based on sentiment score and engagement
5. **Recommendations**: AI generates context-aware response recommendations
6. **Notification**: Critical and High priority alerts are sent via Slack and Email
7. **Dashboard**: All alerts are displayed in a beautiful web dashboard

## 📊 Dashboard Features

- **Real-time Statistics**: Total alerts, critical/high priority counts, 24-hour activity
- **Alert Feed**: View all alerts with filtering by urgency and source
- **Manual Monitoring**: Trigger monitoring checks on-demand
- **Test Alerts**: Send test notifications to verify your Slack/Email setup
- **Auto-refresh**: Dashboard updates automatically every 30 seconds

## 🔧 Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `KEYWORDS` | Comma-separated keywords to monitor | - |
| `CHECK_INTERVAL_MINUTES` | Minutes between monitoring checks | 15 |
| `SENTIMENT_THRESHOLD` | Threshold for negative sentiment (-1 to 0) | -0.3 |
| `FLASK_PORT` | Port for web dashboard | 5000 |

## 🧪 Testing

### Test Sentiment Analysis

```bash
curl -X POST http://localhost:5000/api/test/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "Your product is terrible and buggy!"}'
```

### Test Alert System

Use the dashboard "Test Alerts" button or:

```bash
curl -X POST http://localhost:5000/api/test/alerts
```

This will:
- Create a test alert in the database
- Send a test notification to Slack (if configured)
- Send a test notification to Email (if configured)

### Manual Monitoring Run

Use the dashboard "Run Monitor Now" button or:

```bash
curl -X POST http://localhost:5000/api/monitor/run
```

## 📁 Project Structure

```
Agent-Saad/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Flask application
│   ├── agent.py                 # Agent logic and scheduling
│   ├── models/
│   │   └── sentiment.py         # Sentiment analysis model
│   ├── monitors/
│   │   ├── twitter_monitor.py   # Twitter monitoring
│   │   └── reddit_monitor.py    # Reddit monitoring
│   ├── alerts/
│   │   ├── slack_alert.py       # Slack notifications
│   │   └── email_alert.py       # Email notifications
│   ├── database/
│   │   └── db.py                # SQLite database
│   └── templates/
│       └── dashboard.html       # Dashboard UI
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── dashboard.js
├── .env                          # Configuration (create this)
├── config.py                     # Config loader
├── requirements.txt              # Python dependencies
├── run.py                        # Application entry point
└── README.md
```

## 🔑 Getting API Credentials

### Twitter/X API
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app
3. Generate Bearer Token and API keys
4. Add to `.env` file

### Reddit API
1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Create a new app (script type)
3. Get Client ID and Secret
4. Add to `.env` file

### Slack Bot
1. Go to [Slack API](https://api.slack.com/apps)
2. Create a new app
3. Add OAuth scopes: `chat:write`, `channels:read`
4. Install to workspace and get Bot Token
5. Add to `.env` file

### Email (Gmail)
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password
3. Use the app password in `.env` (not your regular password)

## 🎨 Dashboard Preview

The dashboard features:
- Modern gradient design
- Real-time statistics cards
- Filterable alert feed
- Color-coded urgency levels
- One-click testing and monitoring
- Responsive design for mobile

## 🐛 Troubleshooting

**Q: Sentiment model download is slow**
A: The first run downloads the DistilBERT model (~250MB). Subsequent runs will be fast.

**Q: No alerts appearing**
A: Check that your keywords match actual social media content, and adjust `SENTIMENT_THRESHOLD` if needed.

**Q: Slack/Email not working**
A: Use the "Test Alerts" button to verify configuration. Check logs for error messages.

**Q: Twitter API errors**
A: Verify your Bearer Token is valid and has the required access levels.

## 📝 License

See LICENSE file for details.

## 🤝 Contributing

This is an MVP. Feel free to extend with:
- More social media platforms
- Advanced sentiment models
- Response automation
- Analytics and trends
- Mobile app notifications

## 📧 Support

For issues or questions, check the logs in `agent_saad.log` or review the console output.

---

**Built with ❤️ using Flask, Transformers, and AI**

