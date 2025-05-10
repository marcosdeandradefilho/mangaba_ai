from slack_agent_handler import SlackAgentHandler
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Your bot token
    BOT_TOKEN = "YOUR_SLACK_BOT_TOKEN"
    
    try:
        # Initialize the agent handler
        handler = SlackAgentHandler(bot_token=BOT_TOKEN)
        
        # Register different types of agents with enhanced configurations
        handler.register_agent("analyzer", {
            "name": "Data Analyzer",
            "role": "Analyst",
            "capabilities": ["channel_analysis", "user_activity", "message_patterns"],
            "personality": "analytical"
        })
        
        handler.register_agent("helper", {
            "name": "Assistant",
            "role": "Support",
            "capabilities": ["help", "guidance", "documentation"],
            "personality": "friendly"
        })
        
        handler.register_agent("researcher", {
            "name": "Research Bot",
            "role": "Researcher",
            "capabilities": ["topic_research", "content_summary", "trend_analysis"],
            "personality": "curious"
        })
        
        # Channel ID from your workspace
        CHANNEL_ID = "C01N7HUJ6U9"
        
        # Example: Send an initial message to the channel
        handler.send_agent_message(
            channel_id=CHANNEL_ID,
            agent_id="helper",
            message="Hello! I'm here to help analyze and understand the conversations in this channel. "
                   "You can ask me to:\n"
                   "• Analyze channel content\n"
                   "• Research topics\n"
                   "• Provide insights\n"
                   "• Show trends and patterns\n"
                   "Just mention what you need!"
        )
        
        # Example: Simulate different types of user requests
        example_events = [
            {
                "type": "message",
                "text": "Can you analyze the recent discussions?",
                "channel": CHANNEL_ID,
                "ts": str(time.time()),
                "user": "U01HJQU55T7"
            },
            {
                "type": "message",
                "text": "What are the trends in this channel?",
                "channel": CHANNEL_ID,
                "ts": str(time.time() + 1),
                "user": "U023Y3PCBDX"
            },
            {
                "type": "message",
                "text": "Give me a summary of recent messages",
                "channel": CHANNEL_ID,
                "ts": str(time.time() + 2),
                "user": "U01HJQU55T7"
            }
        ]
        
        # Handle each example event
        for event in example_events:
            print(f"\nProcessing request: {event['text']}")
            handler.handle_message(event)
            time.sleep(2)  # Add delay between messages for readability
        
        # Print agent status
        print("\nRegistered Agents:")
        print("-" * 50)
        for agent in handler.get_agent_status():
            print(f"Name: {agent['name']}")
            print(f"Role: {agent['role']}")
            print(f"Personality: {agent['personality']}")
            print(f"Capabilities: {', '.join(agent['capabilities'])}")
            print("-" * 30)
            
    except Exception as e:
        logger.error(f"Error during agent interaction: {str(e)}")
        print("\nTo fix this error, please ensure:")
        print("1. The bot has been added to the channel")
        print("2. The bot has the following OAuth scopes:")
        print("   - channels:history")
        print("   - chat:write")
        print("   - groups:history")
        print("3. The channel ID is correct")

if __name__ == "__main__":
    main() 