"""
Sentiment Analyzer Module
Handles sentiment analysis for individual messages and conversation history
"""

from typing import Dict, List, Tuple
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    """
    Analyzes sentiment using VADER (Valence Aware Dictionary and sEntiment Reasoner)
    VADER is specifically designed for social media text and performs well on conversational data
    """
    
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        
    def analyze_message(self, message: str) -> Dict[str, any]:
        """
        Analyze sentiment of a single message
        
        Args:
            message: User message text
            
        Returns:
            Dictionary containing sentiment scores and label
        """
        scores = self.analyzer.polarity_scores(message)
        
        # Determine sentiment label based on compound score
        # VADER compound score ranges from -1 (most negative) to +1 (most positive)
        sentiment_label = self._get_sentiment_label(scores['compound'])
        
        return {
            'compound': scores['compound'],
            'positive': scores['pos'],
            'neutral': scores['neu'],
            'negative': scores['neg'],
            'label': sentiment_label
        }
    
    def analyze_conversation(self, messages: List[Tuple[str, str]]) -> Dict[str, any]:
        """
        Analyze overall sentiment of entire conversation
        
        Args:
            messages: List of tuples (role, message_text)
            
        Returns:
            Dictionary with overall sentiment analysis and trends
        """
        user_messages = [msg for role, msg in messages if role == 'user']
        
        if not user_messages:
            return {
                'overall_sentiment': 'Neutral',
                'compound_score': 0.0,
                'message_count': 0,
                'sentiment_distribution': {}
            }
        
        # Analyze each user message
        message_sentiments = [self.analyze_message(msg) for msg in user_messages]
        
        # Calculate average compound score
        avg_compound = sum(s['compound'] for s in message_sentiments) / len(message_sentiments)
        
        # Count sentiment distribution
        sentiment_counts = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
        for sentiment in message_sentiments:
            sentiment_counts[sentiment['label']] += 1
        
        # Detect mood shift (compare first half vs second half)
        mood_shift = self._detect_mood_shift(message_sentiments)
        
        return {
            'overall_sentiment': self._get_sentiment_label(avg_compound),
            'compound_score': round(avg_compound, 3),
            'message_count': len(user_messages),
            'sentiment_distribution': sentiment_counts,
            'mood_shift': mood_shift,
            'individual_scores': message_sentiments
        }
    
    def _get_sentiment_label(self, compound_score: float) -> str:
        """
        Convert compound score to sentiment label
        
        Thresholds:
        - >= 0.05: Positive
        - <= -0.05: Negative
        - Between: Neutral
        """
        if compound_score >= 0.05:
            return 'Positive'
        elif compound_score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    
    def _detect_mood_shift(self, sentiments: List[Dict]) -> str:
        """
        Detect if there's a significant mood shift in conversation
        Compares first half with second half
        """
        if len(sentiments) < 2:
            return "Insufficient data"
        
        mid_point = len(sentiments) // 2
        first_half_avg = sum(s['compound'] for s in sentiments[:mid_point]) / mid_point
        second_half_avg = sum(s['compound'] for s in sentiments[mid_point:]) / (len(sentiments) - mid_point)
        
        diff = second_half_avg - first_half_avg
        
        if diff > 0.2:
            return "Improving (conversation became more positive)"
        elif diff < -0.2:
            return "Declining (conversation became more negative)"
        else:
            return "Stable (consistent mood throughout)"