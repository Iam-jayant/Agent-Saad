"""
Agent Saad - Main Agent Logic
This module handles the monitoring and processing cycle
"""

import logging
from typing import Dict, List
from app.database.db import Database
from app.models.sentiment import SentimentAnalyzer
from app.monitors.twitter_monitor import TwitterMonitor
from app.monitors.reddit_monitor import RedditMonitor
from app.alerts.slack_alert import SlackAlerter
from app.alerts.email_alert import EmailAlerter
from config import Config

logger = logging.getLogger(__name__)

# Initialize components
db = Database(Config.DATABASE_PATH)
sentiment_analyzer = SentimentAnalyzer()
twitter_monitor = TwitterMonitor()
reddit_monitor = RedditMonitor()
slack_alerter = SlackAlerter()
email_alerter = EmailAlerter()

def process_item(item: Dict, source: str) -> bool:
    """
    Process a single social media item for sentiment analysis
    
    Args:
        item: Dictionary containing item data
        source: Source platform (Twitter/Reddit)
    
    Returns:
        bool: True if alert was created, False otherwise
    """
    try:
        item_id = item.get('id')
        text = item.get('text', '')
        
        # Skip if already processed
        if db.is_processed(source, item_id):
            logger.debug(f"Item {item_id} already processed, skipping")
            return False
        
        # Mark as processed
        db.mark_as_processed(source, item_id)
        
        # Skip if no text
        if not text or len(text.strip()) < 10:
            logger.debug(f"Item {item_id} has insufficient text, skipping")
            return False
        
        # Analyze sentiment
        sentiment = sentiment_analyzer.analyze(text)
        
        # Check if sentiment is negative enough to alert
        if sentiment['normalized_score'] > Config.SENTIMENT_THRESHOLD:
            logger.debug(f"Item {item_id} sentiment not negative enough ({sentiment['normalized_score']}), skipping")
            return False
        
        # Determine urgency
        engagement = item.get('engagement', 0)
        urgency = sentiment_analyzer.determine_urgency(sentiment['normalized_score'], engagement)
        
        # Generate recommendation
        recommendation = sentiment_analyzer.generate_response_recommendation(text, sentiment['label'])
        
        # Create alert data
        alert_data = {
            'source': source,
            'content': text,
            'author': item.get('author', 'Unknown'),
            'url': item.get('url', ''),
            'sentiment_score': sentiment['normalized_score'],
            'sentiment_label': sentiment['label'],
            'urgency_level': urgency,
            'recommended_response': recommendation
        }
        
        # Save alert to database
        alert_id = db.add_alert(alert_data)
        logger.info(f"Created alert {alert_id} for item {item_id} with urgency {urgency}")
        
        # Send notifications
        notifications_sent = False
        
        if urgency in ['CRITICAL', 'HIGH']:
            # Send Slack notification
            if slack_alerter.send_alert(alert_data):
                logger.info(f"Slack alert sent for alert {alert_id}")
                notifications_sent = True
            
            # Send Email notification
            if email_alerter.send_alert(alert_data):
                logger.info(f"Email alert sent for alert {alert_id}")
                notifications_sent = True
        
        # Mark as notified if any notification was sent
        if notifications_sent:
            db.mark_as_notified(alert_id)
        
        return True
        
    except Exception as e:
        logger.error(f"Error processing item: {e}")
        return False

def process_monitoring_cycle() -> Dict:
    """
    Run a complete monitoring cycle for all sources
    
    Returns:
        dict: Results summary
    """
    logger.info("Starting monitoring cycle...")
    
    results = {
        'twitter_items': 0,
        'reddit_items': 0,
        'total_processed': 0,
        'alerts_created': 0
    }
    
    try:
        # Monitor Twitter
        if Config.KEYWORDS:
            logger.info(f"Monitoring Twitter for keywords: {Config.KEYWORDS}")
            tweets = twitter_monitor.search_mentions(Config.KEYWORDS, max_results=20)
            results['twitter_items'] = len(tweets)
            
            for tweet in tweets:
                if process_item(tweet, 'Twitter'):
                    results['alerts_created'] += 1
        
        # Monitor Reddit
        if Config.KEYWORDS:
            logger.info(f"Monitoring Reddit for keywords: {Config.KEYWORDS}")
            reddit_posts = reddit_monitor.search_mentions(Config.KEYWORDS, limit=20)
            results['reddit_items'] = len(reddit_posts)
            
            for post in reddit_posts:
                if process_item(post, 'Reddit'):
                    results['alerts_created'] += 1
        
        results['total_processed'] = results['twitter_items'] + results['reddit_items']
        
        logger.info(f"Monitoring cycle completed: {results}")
        return results
        
    except Exception as e:
        logger.error(f"Error in monitoring cycle: {e}")
        return results

def start_scheduled_monitoring():
    """Start the scheduled monitoring agent"""
    from apscheduler.schedulers.background import BackgroundScheduler
    
    scheduler = BackgroundScheduler()
    
    # Schedule monitoring job
    scheduler.add_job(
        process_monitoring_cycle,
        'interval',
        minutes=Config.CHECK_INTERVAL_MINUTES,
        id='monitor_sentiment',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info(f"Scheduled monitoring started (every {Config.CHECK_INTERVAL_MINUTES} minutes)")
    
    return scheduler

