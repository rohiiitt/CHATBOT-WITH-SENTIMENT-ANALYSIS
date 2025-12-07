"""
Unit Tests for Sentiment Analysis Chatbot
"""

import pytest
from sentiment_analyzer import SentimentAnalyzer
from chatbot import SentimentChatbot


class TestSentimentAnalyzer:
    """Test suite for SentimentAnalyzer"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.analyzer = SentimentAnalyzer()
    
    def test_positive_sentiment(self):
        """Test detection of positive sentiment"""
        result = self.analyzer.analyze_message("I love this service! It's amazing!")
        assert result['label'] == 'Positive'
        assert result['compound'] > 0
    
    def test_negative_sentiment(self):
        """Test detection of negative sentiment"""
        result = self.analyzer.analyze_message("This is terrible and disappointing")
        assert result['label'] == 'Negative'
        assert result['compound'] < 0
    
    def test_neutral_sentiment(self):
        """Test detection of neutral sentiment"""
        result = self.analyzer.analyze_message("The product exists")
        assert result['label'] == 'Neutral'
        assert abs(result['compound']) < 0.05
    
    def test_conversation_analysis_empty(self):
        """Test conversation analysis with no messages"""
        result = self.analyzer.analyze_conversation([])
        assert result['overall_sentiment'] == 'Neutral'
        assert result['message_count'] == 0
    
    def test_conversation_analysis_single_message(self):
        """Test conversation analysis with one message"""
        messages = [('user', 'Great service!')]
        result = self.analyzer.analyze_conversation(messages)
        assert result['message_count'] == 1
        assert result['overall_sentiment'] in ['Positive', 'Neutral', 'Negative']
    
    def test_conversation_analysis_mixed_sentiments(self):
        """Test conversation with mixed sentiments"""
        messages = [
            ('user', 'I love it!'),
            ('bot', 'Great!'),
            ('user', 'But it could be better'),
            ('bot', 'I understand')
        ]
        result = self.analyzer.analyze_conversation(messages)
        assert result['message_count'] == 2  # Only counts user messages
        assert 'sentiment_distribution' in result
    
    def test_mood_shift_detection(self):
        """Test mood shift detection"""
        messages = [
            ('user', 'This is terrible'),
            ('bot', 'Sorry'),
            ('user', 'Actually it got better'),
            ('bot', 'Great!')
        ]
        result = self.analyzer.analyze_conversation(messages)
        assert 'mood_shift' in result
    
    def test_sentiment_label_boundaries(self):
        """Test sentiment label threshold boundaries"""
        # Test positive threshold
        assert self.analyzer._get_sentiment_label(0.05) == 'Positive'
        assert self.analyzer._get_sentiment_label(0.06) == 'Positive'
        
        # Test negative threshold
        assert self.analyzer._get_sentiment_label(-0.05) == 'Negative'
        assert self.analyzer._get_sentiment_label(-0.06) == 'Negative'
        
        # Test neutral range
        assert self.analyzer._get_sentiment_label(0.04) == 'Neutral'
        assert self.analyzer._get_sentiment_label(-0.04) == 'Neutral'
        assert self.analyzer._get_sentiment_label(0.0) == 'Neutral'


class TestSentimentChatbot:
    """Test suite for SentimentChatbot"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.chatbot = SentimentChatbot()
    
    def test_initialization(self):
        """Test chatbot initializes correctly"""
        assert len(self.chatbot.conversation_history) == 0
        assert self.chatbot.sentiment_analyzer is not None
    
    def test_process_message(self):
        """Test message processing"""
        response, sentiment = self.chatbot.process_message("Hello!")
        assert response is not None
        assert 'label' in sentiment
        assert len(self.chatbot.conversation_history) == 2  # User + Bot
    
    def test_conversation_history_storage(self):
        """Test conversation history is properly stored"""
        self.chatbot.process_message("First message")
        self.chatbot.process_message("Second message")
        
        history = self.chatbot.get_conversation_history()
        assert len(history) == 4  # 2 user + 2 bot messages
        assert history[0][0] == 'user'
        assert history[1][0] == 'bot'
    
    def test_greeting_detection(self):
        """Test greeting detection in responses"""
        response, _ = self.chatbot.process_message("Hello")
        assert len(response) > 0
    
    def test_farewell_detection(self):
        """Test farewell detection in responses"""
        response, _ = self.chatbot.process_message("Goodbye")
        assert len(response) > 0
    
    def test_negative_sentiment_response(self):
        """Test appropriate response to negative sentiment"""
        response, sentiment = self.chatbot.process_message("This is awful and disappointing")
        assert sentiment['label'] == 'Negative'
        assert len(response) > 0
    
    def test_positive_sentiment_response(self):
        """Test appropriate response to positive sentiment"""
        response, sentiment = self.chatbot.process_message("This is wonderful and amazing!")
        assert sentiment['label'] == 'Positive'
        assert len(response) > 0
    
    def test_conversation_analysis(self):
        """Test full conversation analysis"""
        self.chatbot.process_message("I'm happy")
        self.chatbot.process_message("This is okay")
        self.chatbot.process_message("I'm sad")
        
        analysis = self.chatbot.get_conversation_analysis()
        assert 'overall_sentiment' in analysis
        assert 'compound_score' in analysis
        assert 'sentiment_distribution' in analysis
        assert analysis['message_count'] == 3
    
    def test_reset_conversation(self):
        """Test conversation reset functionality"""
        self.chatbot.process_message("Test message")
        assert len(self.chatbot.conversation_history) > 0
        
        self.chatbot.reset_conversation()
        assert len(self.chatbot.conversation_history) == 0
    
    def test_empty_message_handling(self):
        """Test handling of edge cases"""
        response, sentiment = self.chatbot.process_message("")
        assert response is not None
        assert sentiment is not None
    
    def test_special_topic_detection(self):
        """Test detection of special topics in messages"""
        # Test problem detection
        response1, _ = self.chatbot.process_message("I have a problem with this")
        assert len(response1) > 0
        
        # Test pricing detection
        response2, _ = self.chatbot.process_message("This is too expensive")
        assert len(response2) > 0
        
        # Test thank you detection
        response3, _ = self.chatbot.process_message("Thank you so much")
        assert len(response3) > 0


class TestIntegration:
    """Integration tests for complete workflow"""
    
    def test_full_conversation_flow(self):
        """Test complete conversation flow from start to finish"""
        chatbot = SentimentChatbot()
        
        # Simulate a conversation
        messages = [
            "Hello!",
            "Your service is disappointing",
            "Last experience was better",
            "Thanks for listening"
        ]
        
        for msg in messages:
            chatbot.process_message(msg)
        
        # Get analysis
        analysis = chatbot.get_conversation_analysis()
        
        # Verify analysis structure
        assert analysis['message_count'] == len(messages)
        assert 'overall_sentiment' in analysis
        assert 'sentiment_distribution' in analysis
        assert 'mood_shift' in analysis
        assert len(analysis['individual_scores']) == len(messages)
    
    def test_sentiment_accuracy_with_known_phrases(self):
        """Test sentiment detection with known sentiment phrases"""
        analyzer = SentimentAnalyzer()
        
        # Strongly positive
        result1 = analyzer.analyze_message("I absolutely love this! It's perfect!")
        assert result1['label'] == 'Positive'
        
        # Strongly negative
        result2 = analyzer.analyze_message("I hate this! It's completely broken!")
        assert result2['label'] == 'Negative'
        
        # Mixed/neutral
        result3 = analyzer.analyze_message("It's okay, nothing special")
        assert result3['compound'] > -0.5 and result3['compound'] < 0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=.", "--cov-report=term-missing"])