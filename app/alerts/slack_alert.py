import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import Config

logger = logging.getLogger(__name__)

class SlackAlerter:
    def __init__(self):
        self.client = None
        self.channel = Config.SLACK_CHANNEL
        self.setup_client()
    
    def setup_client(self):
        """Setup Slack client"""
        try:
            if Config.SLACK_BOT_TOKEN:
                self.client = WebClient(token=Config.SLACK_BOT_TOKEN)
                logger.info("Slack client initialized successfully")
            else:
                logger.warning("Slack bot token not configured")
        except Exception as e:
            logger.error(f"Failed to initialize Slack client: {e}")
    
    def send_alert(self, alert_data: dict) -> bool:
        """
        Send an alert to Slack
        
        Args:
            alert_data: Dictionary containing alert information
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.client:
            logger.warning("Slack client not initialized, skipping alert")
            return False
        
        try:
            # Determine urgency emoji and color
            urgency = alert_data.get('urgency_level', 'LOW')
            urgency_emoji = {
                'CRITICAL': '🚨',
                'HIGH': '⚠️',
                'MEDIUM': '⚡',
                'LOW': 'ℹ️'
            }.get(urgency, 'ℹ️')
            
            color = {
                'CRITICAL': '#FF0000',
                'HIGH': '#FF6600',
                'MEDIUM': '#FFCC00',
                'LOW': '#0099CC'
            }.get(urgency, '#0099CC')
            
            # Build message blocks
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{urgency_emoji} New Sentiment Alert - {urgency} Priority"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Source:*\n{alert_data.get('source', 'Unknown')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Author:*\n{alert_data.get('author', 'Unknown')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Sentiment:*\n{alert_data.get('sentiment_label', 'Unknown')} ({alert_data.get('sentiment_score', 0):.2f})"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Urgency:*\n{urgency}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Content:*\n```{alert_data.get('content', '')[:500]}```"
                    }
                }
            ]
            
            # Add recommended response if available
            if alert_data.get('recommended_response'):
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Recommended Response:*\n{alert_data.get('recommended_response')}"
                    }
                })
            
            # Add link if available
            if alert_data.get('url'):
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<{alert_data.get('url')}|View Original Post>"
                    }
                })
            
            # Add divider
            blocks.append({"type": "divider"})
            
            # Send message
            response = self.client.chat_postMessage(
                channel=self.channel,
                blocks=blocks,
                text=f"New {urgency} sentiment alert from {alert_data.get('source')}"
            )
            
            logger.info(f"Slack alert sent successfully: {response['ts']}")
            return True
            
        except SlackApiError as e:
            logger.error(f"Slack API error: {e.response['error']}")
            return False
        except Exception as e:
            logger.error(f"Error sending Slack alert: {e}")
            return False
    
    def send_test_alert(self) -> bool:
        """Send a test alert to verify Slack integration"""
        test_data = {
            'source': 'Test',
            'author': 'Agent Saad',
            'content': 'This is a test alert from Agent Saad Customer Sentiment Alert System.',
            'sentiment_score': -0.5,
            'sentiment_label': 'NEGATIVE',
            'urgency_level': 'MEDIUM',
            'recommended_response': 'This is a test - no action required.',
            'url': 'https://github.com'
        }
        return self.send_alert(test_data)

