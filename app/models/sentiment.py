from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SentimentAnalyzer, cls).__new__(cls)
            cls._instance.init_model()
        return cls._instance
    
    def init_model(self):
        """Initialize the sentiment analysis model"""
        try:
            # Using distilbert-base-uncased-finetuned-sst-2-english (free and fast)
            logger.info("Loading sentiment analysis model...")
            import torch
            self.classifier = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                framework="pt",  # Explicitly use PyTorch
                device=-1  # Use CPU (-1), for GPU use 0
            )
            logger.info("Sentiment analysis model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load sentiment model: {e}")
            raise
    
    def analyze(self, text: str) -> dict:
        """
        Analyze sentiment of given text
        
        Returns:
            dict: {
                'label': 'POSITIVE' or 'NEGATIVE',
                'score': float between 0 and 1,
                'normalized_score': float between -1 and 1
            }
        """
        try:
            if not text or len(text.strip()) == 0:
                return {
                    'label': 'NEUTRAL',
                    'score': 0.5,
                    'normalized_score': 0.0
                }
            
            # Truncate text if too long (model limit is 512 tokens)
            text = text[:500]
            
            result = self.classifier(text)[0]
            
            # Normalize score to -1 (very negative) to 1 (very positive)
            if result['label'] == 'NEGATIVE':
                normalized_score = -(result['score'])
            else:
                normalized_score = result['score']
            
            return {
                'label': result['label'],
                'score': result['score'],
                'normalized_score': normalized_score
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                'label': 'ERROR',
                'score': 0.0,
                'normalized_score': 0.0
            }
    
    def determine_urgency(self, sentiment_score: float, engagement: int = 0) -> str:
        """
        Determine urgency level based on sentiment score and engagement
        
        Args:
            sentiment_score: Normalized score between -1 and 1
            engagement: Number of likes, retweets, upvotes, etc.
        
        Returns:
            str: 'CRITICAL', 'HIGH', 'MEDIUM', or 'LOW'
        """
        if sentiment_score <= -0.7:
            if engagement > 100:
                return 'CRITICAL'
            else:
                return 'HIGH'
        elif sentiment_score <= -0.3:
            if engagement > 50:
                return 'HIGH'
            else:
                return 'MEDIUM'
        elif sentiment_score <= 0:
            return 'LOW'
        else:
            return 'LOW'
    
    def generate_response_recommendation(self, text: str, sentiment_label: str) -> str:
        """
        Generate a recommended response based on the content and sentiment
        
        Args:
            text: The original text/complaint
            sentiment_label: POSITIVE or NEGATIVE
        
        Returns:
            str: Recommended response strategy
        """
        text_lower = text.lower()
        
        # Detect specific issues
        if 'bug' in text_lower or 'error' in text_lower or 'crash' in text_lower:
            return "Technical Issue: Acknowledge the bug, provide workaround if available, and escalate to engineering team."
        
        elif 'refund' in text_lower or 'money back' in text_lower or 'cancel' in text_lower:
            return "Billing Concern: Review account, offer resolution options, escalate to billing department if needed."
        
        elif 'slow' in text_lower or 'down' in text_lower or 'not working' in text_lower:
            return "Performance Issue: Check system status, provide troubleshooting steps, escalate if widespread."
        
        elif 'support' in text_lower or 'help' in text_lower or 'customer service' in text_lower:
            return "Support Request: Respond promptly with helpful resources, offer direct assistance."
        
        elif 'hate' in text_lower or 'terrible' in text_lower or 'worst' in text_lower:
            return "Strong Negative: Respond empathetically, offer to discuss privately, involve senior support."
        
        else:
            if sentiment_label == 'NEGATIVE':
                return "General Negative Feedback: Thank for feedback, apologize for experience, offer to help resolve."
            else:
                return "Monitor: No immediate action required, but track for trends."

