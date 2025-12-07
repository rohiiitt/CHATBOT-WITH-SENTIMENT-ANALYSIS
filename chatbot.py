"""
Chatbot Module
Handles conversation flow and response generation
"""

from typing import List, Tuple
import random
from sentiment_analyzer import SentimentAnalyzer


class SentimentChatbot:
    """
    A chatbot that maintains conversation history and provides sentiment-aware responses
    """
    
    def __init__(self):
        self.conversation_history: List[Tuple[str, str]] = []
        self.sentiment_analyzer = SentimentAnalyzer()
        self.user_name = None
        
        # Response templates categorized by sentiment
        self.responses = {
            'Positive': [
                "That's wonderful to hear! I'm glad you're having a positive experience.",
                "Great! I'm happy to help you further.",
                "Excellent! Your satisfaction is important to us.",
                "That's fantastic! How else can I assist you today?",
                "I'm thrilled to hear that! Let me know if there's anything else."
            ],
            'Negative': [
                "I understand your frustration. Let me help resolve this for you.",
                "I apologize for the inconvenience. I'll make sure your concern is addressed.",
                "I'm sorry to hear that. Your feedback is valuable and I want to make this right.",
                "I hear your concerns. Let's work together to find a solution.",
                "I appreciate you bringing this to my attention. How can I improve your experience?"
            ],
            'Neutral': [
                "I understand. How can I assist you further?",
                "Thank you for sharing. What else would you like to know?",
                "Got it. Is there anything specific I can help with?",
                "I see. Let me know what you need.",
                "Understood. Feel free to ask me anything."
            ],
            'greeting': [
                "Hello! I'm here to help you. How are you doing today?",
                "Hi there! Welcome! What can I do for you?",
                "Greetings! I'm ready to assist you with anything you need.",
                "Hey! Great to chat with you. What's on your mind?"
            ],
            'farewell': [
                "Thank you for chatting with me! Have a wonderful day!",
                "Goodbye! Feel free to reach out anytime.",
                "Take care! It was nice talking with you.",
                "Farewell! Hope to chat again soon!"
            ]
        }
    
    def process_message(self, user_message: str) -> Tuple[str, dict]:
        """
        Process user message and generate appropriate response
        
        Args:
            user_message: The message from the user
            
        Returns:
            Tuple of (bot_response, sentiment_analysis)
        """
        # Analyze sentiment of user message
        sentiment = self.sentiment_analyzer.analyze_message(user_message)
        
        # Store in conversation history
        self.conversation_history.append(('user', user_message))
        
        # Generate response based on sentiment and content
        bot_response = self._generate_response(user_message, sentiment['label'])
        
        # Store bot response in history
        self.conversation_history.append(('bot', bot_response))
        
        return bot_response, sentiment
    
    def _generate_response(self, message: str, sentiment_label: str) -> str:
        """
        Generate contextually appropriate response
        """
        message_lower = message.lower()
        
        # Check for greetings
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            if not self.user_name:
                return random.choice(self.responses['greeting'])
        
        # Check for farewells
        if any(word in message_lower for word in ['bye', 'goodbye', 'farewell', 'see you']):
            return random.choice(self.responses['farewell'])
        
        # Check for specific topics and provide contextual responses
        if any(word in message_lower for word in ['problem', 'issue', 'bug', 'error', 'broken']):
            return "I'm sorry you're experiencing technical difficulties. Can you provide more details so I can help resolve this?"
        
        if any(word in message_lower for word in ['price', 'cost', 'expensive', 'cheap']):
            if sentiment_label == 'Negative':
                return "I understand pricing is a concern. Let me see what options might work better for your budget."
            else:
                return "I'm happy to discuss pricing options that fit your needs."
        
        if any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
            return "You're very welcome! Is there anything else I can help you with?"
        
        # Default to sentiment-based response
        return random.choice(self.responses.get(sentiment_label, self.responses['Neutral']))
    
    def get_conversation_history(self) -> List[Tuple[str, str]]:
        """Return full conversation history"""
        return self.conversation_history
    
    def get_conversation_analysis(self) -> dict:
        """Get comprehensive sentiment analysis of entire conversation"""
        return self.sentiment_analyzer.analyze_conversation(self.conversation_history)
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.user_name = None