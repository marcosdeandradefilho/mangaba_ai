import os
from dotenv import load_dotenv
from mangaba_channel_analyzer import MangabaChannelAnalyzer
import logging
from datetime import datetime, timedelta
from slack_sdk.errors import SlackApiError
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def format_analysis_results(analysis):
    """Format analysis results into a readable string."""
    output = []
    output.append("\nChannel Analysis Results:")
    output.append("=" * 50)
    output.append(f"Total Messages: {analysis['total_messages']}")
    output.append(f"Unique Users: {analysis['unique_users']}")
    output.append(f"Most Active Time: {analysis.get('most_active_time', 'N/A')}")
    
    output.append("\nTopic Distribution:")
    for topic, count in analysis["topics"].items():
        output.append(f"• {topic.title()}: {count}")
    
    output.append("\nTop Contributors:")
    for user, count in sorted(analysis["user_activity"].items(), key=lambda x: x[1], reverse=True)[:5]:
        output.append(f"• User {user}: {count} messages")
    
    return "\n".join(output)

def save_to_file(analysis, filename="channel_analysis.txt"):
    """Save analysis results to a file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(format_analysis_results(analysis))
        print(f"\nAnalysis saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {str(e)}")

def send_to_slack(analyzer, channel_id, analysis):
    """Send analysis results to Slack channel."""
    try:
        # Send detailed analysis
        analyzer.handler.send_agent_message(
            channel_id=channel_id,
            agent_id="comm_analyzer",
            message="Channel Analysis Complete! Here are the insights:",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Channel Analysis Report*\n\n" +
                                f"• Total Messages: {analysis['total_messages']}\n" +
                                f"• Unique Contributors: {analysis['unique_users']}\n" +
                                f"• Most Active Time: {analysis.get('most_active_time', 'N/A')}"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Topic Distribution:*\n" +
                                f"• Code Discussions: {analysis['topics']['code']}\n" +
                                f"• Architecture: {analysis['topics']['architecture']}\n" +
                                f"• Integration: {analysis['topics']['integration']}\n" +
                                f"• Planning: {analysis['topics']['planning']}\n" +
                                f"• Other: {analysis['topics']['other']}"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Top Contributors:*\n" +
                                "\n".join(
                                    f"• <@{user}>: {count} messages"
                                    for user, count in sorted(
                                        analysis["user_activity"].items(),
                                        key=lambda x: x[1],
                                        reverse=True
                                    )[:5]
                                )
                    }
                }
            ]
        )
        print("\nAnalysis sent to Slack channel")
    except Exception as e:
        print(f"Error sending to Slack: {str(e)}")

def analyze_mangaba_channel(output_type="terminal"):
    """
    Analyze the Mangaba Slack channel using specialized agents.
    
    Args:
        output_type (str): Where to display results ('terminal', 'slack', 'file', or 'all')
    """
    try:
        # Initialize the analyzer with bot token
        bot_token = os.getenv('SLACK_BOT_TOKEN')
        channel_id = os.getenv('SLACK_CHANNEL_ID')
        
        if not bot_token or not channel_id:
            raise ValueError("Missing required environment variables: SLACK_BOT_TOKEN or SLACK_CHANNEL_ID")
        
        analyzer = MangabaChannelAnalyzer(
            bot_token=bot_token,
            workspace_id="T013NTSNZSP",
            channel_id=channel_id
        )
        
        # Register specialized agents for Mangaba analysis
        analyzer.handler.register_agent("repo_analyzer", {
            "name": "Mangaba Repository Analyzer",
            "role": "Code Analyst",
            "capabilities": ["code_analysis", "architecture_review", "dependency_check"],
            "personality": "technical"
        })
        
        analyzer.handler.register_agent("comm_analyzer", {
            "name": "Communication Analyst",
            "role": "Communication Expert",
            "capabilities": ["message_analysis", "topic_tracking", "engagement_metrics"],
            "personality": "analytical"
        })
        
        analyzer.handler.register_agent("integration_expert", {
            "name": "Integration Specialist",
            "role": "Integration Expert",
            "capabilities": ["slack_integration", "api_analysis", "system_connectivity"],
            "personality": "systematic"
        })
        
        # Get channel messages directly
        try:
            result = analyzer.handler.client.conversations_history(
                channel=channel_id,
                limit=1000
            )
            
            if not result["ok"]:
                raise Exception(f"Failed to get channel messages: {result.get('error')}")
                
            messages = result["messages"]
            
            # Analyze messages
            analysis = {
                "total_messages": len(messages),
                "unique_users": len(set(msg.get("user") for msg in messages if msg.get("user"))),
                "topics": {
                    "code": 0,
                    "architecture": 0,
                    "integration": 0,
                    "planning": 0,
                    "other": 0
                },
                "user_activity": {},
                "time_distribution": {}
            }
            
            # Analyze each message
            for msg in messages:
                text = msg.get("text", "").lower()
                user = msg.get("user")
                timestamp = msg.get("ts")
                
                # Track user activity
                if user:
                    analysis["user_activity"][user] = analysis["user_activity"].get(user, 0) + 1
                
                # Track time distribution
                if timestamp:
                    msg_time = datetime.fromtimestamp(float(timestamp))
                    hour = msg_time.hour
                    analysis["time_distribution"][hour] = analysis["time_distribution"].get(hour, 0) + 1
                
                # Categorize topics
                if any(word in text for word in ["code", "function", "class", "method"]):
                    analysis["topics"]["code"] += 1
                elif any(word in text for word in ["architecture", "design", "structure"]):
                    analysis["topics"]["architecture"] += 1
                elif any(word in text for word in ["integration", "api", "connect"]):
                    analysis["topics"]["integration"] += 1
                elif any(word in text for word in ["plan", "roadmap", "sprint"]):
                    analysis["topics"]["planning"] += 1
                else:
                    analysis["topics"]["other"] += 1
            
            # Find most active time
            if analysis["time_distribution"]:
                most_active_hour = max(analysis["time_distribution"].items(), key=lambda x: x[1])[0]
                analysis["most_active_time"] = f"{most_active_hour:02d}:00"
            
            # Output results based on user choice
            if output_type in ["terminal", "all"]:
                print(format_analysis_results(analysis))
            
            if output_type in ["slack", "all"]:
                send_to_slack(analyzer, channel_id, analysis)
            
            if output_type in ["file", "all"]:
                save_to_file(analysis)
            
            return analysis
            
        except SlackApiError as e:
            logger.error(f"Slack API Error: {str(e)}")
            if e.response["error"] == "missing_scope":
                print("\nError: Bot is missing required permissions.")
                print("Please add the following scopes to your Slack app:")
                print("- chat:write")
                print("- channels:history")
                print("- groups:history")
            raise
            
    except Exception as e:
        logger.error(f"Error during channel analysis: {str(e)}")
        raise

def main():
    """Main function to run the channel analysis."""
    parser = argparse.ArgumentParser(description='Analyze Slack channel and display results')
    parser.add_argument('--output', choices=['terminal', 'slack', 'file', 'all'],
                      default='terminal', help='Where to display results')
    args = parser.parse_args()
    
    try:
        print("\nStarting Mangaba Channel Analysis...")
        print("=" * 50)
        
        result = analyze_mangaba_channel(output_type=args.output)
        
        print("\nAnalysis completed successfully! 🎉")
        
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        print("Please check the logs for more details.")

if __name__ == "__main__":
    main() 