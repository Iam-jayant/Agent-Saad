# 🚀 Agent Saad - Complete Setup Guide

This guide will walk you through setting up Agent Saad from scratch.

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note**: The first time you run the application, it will download the DistilBERT sentiment analysis model (~250MB). This is a one-time download.

## Step 2: Get Twitter/X API Credentials

1. Go to https://developer.twitter.com/
2. Sign in with your Twitter account
3. Click "Create Project" or use existing project
4. Create a new App
5. Go to the "Keys and Tokens" tab
6. Generate and save:
   - API Key (Consumer Key)
   - API Secret (Consumer Secret)
   - Access Token
   - Access Token Secret
   - Bearer Token (most important for search)

**Important**: You need Twitter API v2 access with Essential level (free tier works).

## Step 3: Get Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Scroll to bottom and click "Create App" or "Create Another App"
3. Fill in:
   - Name: Agent-Saad
   - Choose "script"
   - Description: Customer sentiment monitoring
   - About URL: (leave blank)
   - Redirect URI: http://localhost:8080
4. Click "Create App"
5. Save the credentials shown:
   - Client ID (under the app name)
   - Client Secret (next to "secret")

## Step 4: Set Up Slack (Optional but Recommended)

1. Go to https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name it "Agent Saad" and select your workspace
4. In "OAuth & Permissions":
   - Add Bot Token Scopes:
     - `chat:write`
     - `channels:read`
     - `groups:read`
   - Click "Install to Workspace"
   - Authorize the app
   - Copy the "Bot User OAuth Token" (starts with `xoxb-`)
5. Add the bot to your alerts channel:
   - In Slack, go to the channel (e.g., #alerts)
   - Type `/invite @Agent Saad`

## Step 5: Set Up Email (Optional but Recommended)

### For Gmail:

1. Enable 2-Factor Authentication:
   - Go to Google Account settings
   - Security → 2-Step Verification → Turn On

2. Generate App Password:
   - Go to Security → 2-Step Verification
   - Scroll down to "App passwords"
   - Select "Mail" and "Other (Custom name)"
   - Name it "Agent Saad"
   - Click "Generate"
   - Copy the 16-character password

3. Use these settings in `.env`:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_16_char_app_password
   ```

### For Other Email Providers:

**Outlook/Office 365:**
```
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
```

**Yahoo:**
```
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

## Step 6: Configure Environment Variables

Edit the `.env` file in the project root:

```bash
# Twitter/X API Credentials
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_SECRET=your_access_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here

# Reddit API Credentials
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=Agent-Saad/1.0

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
ALERT_EMAIL_TO=team@yourcompany.com

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_CHANNEL=#alerts

# Monitoring Configuration
KEYWORDS=your_brand,your_product,company_name
CHECK_INTERVAL_MINUTES=15
SENTIMENT_THRESHOLD=-0.3

# Flask Configuration
FLASK_SECRET_KEY=change_this_to_random_string
FLASK_PORT=5000
FLASK_DEBUG=True
```

### Important Configuration Notes:

**KEYWORDS**: Comma-separated list of terms to monitor
- Be specific to avoid noise
- Include brand names, product names, variations
- Example: `MyBrand,MyProduct,@MyBrandHandle`

**SENTIMENT_THRESHOLD**: Range from -1 (most negative) to 0 (neutral)
- `-0.3` = moderately negative (recommended)
- `-0.5` = quite negative (fewer alerts)
- `-0.1` = slightly negative (more alerts)

**CHECK_INTERVAL_MINUTES**: How often to check social media
- Minimum: 5 minutes (to avoid rate limits)
- Recommended: 15-30 minutes
- Lower = more real-time but uses more API calls

## Step 7: Run the Application

```bash
python run.py
```

You should see:
```
============================================================
Starting Agent Saad - Customer Sentiment Alert System
============================================================
Loading sentiment analysis model...
Sentiment analysis model loaded successfully
Twitter client initialized successfully
Reddit client initialized successfully
Slack client initialized successfully
Scheduled monitoring started (every 15 minutes)
Starting web dashboard on http://localhost:5000
============================================================
```

## Step 8: Test the Setup

1. Open your browser to `http://localhost:5000`

2. Click "Test Alerts" button
   - This creates a test alert
   - Sends test message to Slack (if configured)
   - Sends test email (if configured)
   - Check you received both!

3. Click "Run Monitor Now" button
   - Searches Twitter and Reddit for your keywords
   - Analyzes sentiment of any mentions
   - Creates alerts for negative sentiment

4. Check the dashboard for any alerts created

## Step 9: Verify Everything Works

✅ **Checklist:**
- [ ] Dashboard loads without errors
- [ ] Test alert appears in dashboard
- [ ] Test Slack message received
- [ ] Test email received
- [ ] Manual monitor run finds social media posts
- [ ] Negative sentiment posts create alerts
- [ ] Alert urgency levels are correct

## Troubleshooting

### "Twitter client not initialized"
- Check your Bearer Token is correct
- Verify you have Twitter API v2 access
- Check for spaces or quotes in your token

### "Reddit client not initialized"
- Verify Client ID and Secret are correct
- Make sure there are no extra spaces
- Check you're using "script" app type

### "No alerts sent" (Slack/Email)
- Verify credentials are correct
- For Slack: bot must be invited to channel
- For Gmail: must use App Password, not regular password
- Check `agent_saad.log` for detailed error messages

### "No alerts appearing"
- Check your keywords match real social media content
- Try searching Twitter/Reddit manually with your keywords
- Lower the sentiment threshold to -0.1 for testing
- Run monitor during active hours

### Model Download Issues
- Ensure stable internet connection
- Model downloads automatically on first run
- Takes 2-5 minutes depending on connection
- Cached locally after first download

## Advanced Configuration

### Custom Sentiment Threshold per Keyword

Currently all keywords use the same threshold. To customize:

Edit `app/agent.py` and add keyword-specific logic in the `process_item` function.

### Add More Social Platforms

To add more platforms (e.g., Facebook, Instagram):
1. Create new monitor in `app/monitors/`
2. Follow the pattern of Twitter/Reddit monitors
3. Add to monitoring cycle in `app/agent.py`

### Change Alert Frequency

Edit urgency conditions in `app/models/sentiment.py`:
```python
def determine_urgency(self, sentiment_score: float, engagement: int = 0) -> str:
    # Customize these thresholds
    if sentiment_score <= -0.7:  # Very negative
        return 'CRITICAL'
    # ... etc
```

## Production Deployment

For production use:

1. **Set `FLASK_DEBUG=False`** in `.env`

2. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app.main:app
   ```

3. **Set up systemd service** (Linux):
   Create `/etc/systemd/system/agent-saad.service`

4. **Use environment variables** instead of `.env` file

5. **Set up HTTPS** with nginx/Apache reverse proxy

6. **Monitor logs** and set up log rotation

7. **Use PostgreSQL** instead of SQLite for better concurrency

## Support

If you encounter issues:

1. Check `agent_saad.log` for detailed error messages
2. Verify all API credentials are correct
3. Test each component individually using test endpoints
4. Ensure Python 3.8+ is installed
5. Try with a single keyword first

---

**Now you're ready to monitor customer sentiment! 🚀**

