"""
Main Entry Point for Sentiment Analysis Chatbot
Provides CLI interface for interaction
"""

import sys
from chatbot import SentimentChatbot
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)


class ChatbotCLI:
    """Command-line interface for the chatbot"""
    
    def __init__(self):
        self.chatbot = SentimentChatbot()
        self.show_tier2 = True  # Enable Tier 2 (statement-level analysis)
        
    def display_welcome(self):
        """Display welcome message"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}  SENTIMENT ANALYSIS CHATBOT")
        print(f"{Fore.CYAN}{'='*70}")
        print(f"{Fore.GREEN}\n✓ Tier 1: Conversation-level sentiment analysis")
        print(f"{Fore.GREEN}✓ Tier 2: Statement-level sentiment analysis")
        print(f"\n{Fore.YELLOW}Type 'quit' or 'exit' to end conversation and see analysis")
        print(f"{Fore.YELLOW}Type 'toggle' to enable/disable statement-level sentiment display")
        print(f"{Fore.CYAN}{'='*70}\n")
    
    def display_sentiment(self, sentiment: dict):
        """Display sentiment with color coding"""
        label = sentiment['label']
        compound = sentiment['compound']
        
        # Color code based on sentiment
        if label == 'Positive':
            color = Fore.GREEN
        elif label == 'Negative':
            color = Fore.RED
        else:
            color = Fore.YELLOW
        
        print(f"{color}→ Sentiment: {label} (score: {compound:.3f})")
    
    def display_conversation_analysis(self):
        """Display comprehensive conversation analysis (Tier 1 + Tier 2 enhancements)"""
        analysis = self.chatbot.get_conversation_analysis()
        
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}  CONVERSATION ANALYSIS")
        print(f"{Fore.CYAN}{'='*70}\n")
        
        # Overall sentiment (Tier 1 requirement)
        overall = analysis['overall_sentiment']
        if overall == 'Positive':
            color = Fore.GREEN
        elif overall == 'Negative':
            color = Fore.RED
        else:
            color = Fore.YELLOW
        
        print(f"{Fore.WHITE}Overall Conversation Sentiment: {color}{overall}")
        print(f"{Fore.WHITE}Compound Score: {color}{analysis['compound_score']}")
        print(f"{Fore.WHITE}Total User Messages: {analysis['message_count']}\n")
        
        # Sentiment distribution
        print(f"{Fore.CYAN}Sentiment Distribution:")
        dist = analysis['sentiment_distribution']
        for sentiment_type, count in dist.items():
            if sentiment_type == 'Positive':
                color = Fore.GREEN
            elif sentiment_type == 'Negative':
                color = Fore.RED
            else:
                color = Fore.YELLOW
            
            percentage = (count / analysis['message_count'] * 100) if analysis['message_count'] > 0 else 0
            print(f"  {color}{sentiment_type}: {count} messages ({percentage:.1f}%)")
        
        # Mood shift analysis (Tier 2 enhancement)
        print(f"\n{Fore.CYAN}Mood Shift Analysis:")
        print(f"{Fore.WHITE}  {analysis['mood_shift']}")
        
        # Message-by-message breakdown (Tier 2)
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}  MESSAGE-BY-MESSAGE BREAKDOWN (TIER 2)")
        print(f"{Fore.CYAN}{'='*70}\n")
        
        history = self.chatbot.get_conversation_history()
        user_msg_index = 0
        
        for role, message in history:
            if role == 'user':
                sentiment = analysis['individual_scores'][user_msg_index]
                label = sentiment['label']
                
                if label == 'Positive':
                    color = Fore.GREEN
                elif label == 'Negative':
                    color = Fore.RED
                else:
                    color = Fore.YELLOW
                
                print(f"{Fore.WHITE}User: \"{message}\"")
                print(f"{color}  → Sentiment: {label} (score: {sentiment['compound']:.3f})\n")
                user_msg_index += 1
        
        print(f"{Fore.CYAN}{'='*70}\n")
    
    def run(self):
        """Main conversation loop"""
        self.display_welcome()
        
        while True:
            try:
                # Get user input
                user_input = input(f"{Fore.BLUE}You: {Style.RESET_ALL}").strip()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print(f"\n{Fore.CYAN}Ending conversation...\n")
                    break
                
                # Check for toggle command
                if user_input.lower() == 'toggle':
                    self.show_tier2 = not self.show_tier2
                    status = "enabled" if self.show_tier2 else "disabled"
                    print(f"{Fore.YELLOW}Statement-level sentiment display {status}\n")
                    continue
                
                # Process message through chatbot
                bot_response, sentiment = self.chatbot.process_message(user_input)
                
                # Display sentiment analysis (Tier 2)
                if self.show_tier2:
                    self.display_sentiment(sentiment)
                
                # Display bot response
                print(f"{Fore.MAGENTA}Bot: {Style.RESET_ALL}{bot_response}\n")
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.CYAN}Conversation interrupted...\n")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}\n")
                continue
        
        # Display final analysis if there were messages
        if len(self.chatbot.get_conversation_history()) > 0:
            self.display_conversation_analysis()
        else:
            print(f"{Fore.YELLOW}No conversation to analyze.\n")


def main():
    """Entry point"""
    cli = ChatbotCLI()
    cli.run()


if __name__ == "__main__":
    main()