@echo off

:: Set Slack environment variables
set SLACK_BOT_TOKEN=YOUR_SLACK_BOT_TOKEN
set SLACK_WORKSPACE_ID=T013NTSNZSP
set SLACK_CHANNEL_ID=C01N7HUJ6U9

:: Print confirmation
echo Environment variables set:
echo SLACK_BOT_TOKEN: %SLACK_BOT_TOKEN:~0,10%...
echo SLACK_WORKSPACE_ID: %SLACK_WORKSPACE_ID%
echo SLACK_CHANNEL_ID: %SLACK_CHANNEL_ID%

:: Run the analyzer
echo.
echo Running Mangaba Channel Analyzer...
python src/integrations/slack/mangaba_channel_analyzer.py 