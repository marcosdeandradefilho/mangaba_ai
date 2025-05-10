from slack_channel_analyzer import SlackChannelAnalyzer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Your bot token
    BOT_TOKEN = "YOUR_SLACK_BOT_TOKEN"
    
    try:
        # Initialize the analyzer with the bot token
        analyzer = SlackChannelAnalyzer(bot_token=BOT_TOKEN)
        
        # Specific channel ID from the workspace
        CHANNEL_ID = "C01N7HUJ6U9"
        
        print(f"\nAnalyzing channel ID: {CHANNEL_ID}")
        
        # Analyze the channel
        analysis = analyzer.analyze_channel(CHANNEL_ID, days=7)
        
        # Print the analysis results
        print("\nChannel Analysis Results:")
        print("-" * 50)
        print(f"Channel ID: {analysis['channel_id']}")
        print(f"Total Messages: {analysis['total_messages']}")
        print(f"Unique Users: {analysis['unique_users']}")
        
        print("\nMessage Types:")
        for msg_type, count in analysis['message_types'].items():
            print(f"- {msg_type}: {count}")
            
        print("\nTime Distribution:")
        for period, count in analysis['time_distribution'].items():
            print(f"- {period}: {count}")
            
        print("\nTop Active Users:")
        # Sort users by message count
        sorted_users = sorted(
            analysis['user_activity'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        for user, count in sorted_users[:5]:  # Show top 5 users
            print(f"- User {user}: {count} messages")
            
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        print("\nTo fix this error, please ensure:")
        print("1. The bot has been added to the channel")
        print("2. The bot has the following OAuth scopes:")
        print("   - channels:history")
        print("   - groups:history")
        print("   - im:history")
        print("   - mpim:history")
        print("3. The channel ID is correct")

if __name__ == "__main__":
    main() 