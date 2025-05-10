# Set up environment variables
$env:SLACK_BOT_TOKEN = 'YOUR_SLACK_BOT_TOKEN'
$env:SLACK_CHANNEL_ID = 'YOUR_CHANNEL_ID'

# Install dependencies if needed
Write-Host "`nChecking dependencies..."
pip install -r requirements.txt

# Create a virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "`nCreating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..."
.\venv\Scripts\Activate.ps1

# Install dependencies in virtual environment
Write-Host "`nInstalling dependencies in virtual environment..."
pip install -r requirements.txt

# Run the tests
Write-Host "`nRunning Slack Integration Tests..."
Write-Host "=" * 50

# Run the test file directly
python test_slack.py

# Check if tests passed
if ($LASTEXITCODE -eq 0) {
    Write-Host "`nAll tests passed successfully! 🎉" -ForegroundColor Green
} else {
    Write-Host "`nSome tests failed. Please check the output above. ❌" -ForegroundColor Red
}

# Deactivate virtual environment
deactivate 