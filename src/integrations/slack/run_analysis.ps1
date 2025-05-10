# Set up environment variables
$env:SLACK_BOT_TOKEN = 'YOUR_SLACK_BOT_TOKEN'
$env:SLACK_CHANNEL_ID = 'C01N7HUJ6U9'

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

# Ask user for output type
Write-Host "`nWhere would you like to see the analysis results?"
Write-Host "1. Terminal (default)"
Write-Host "2. Slack Channel"
Write-Host "3. Text File"
Write-Host "4. All of the above"
$choice = Read-Host "Enter your choice (1-4)"

# Map choice to output type
$output_type = switch ($choice) {
    "2" { "slack" }
    "3" { "file" }
    "4" { "all" }
    default { "terminal" }
}

# Run the analysis
Write-Host "`nRunning Mangaba Channel Analysis..."
Write-Host "=" * 50

# Run the analysis script with selected output type
python mangaba_channel_analysis.py --output $output_type

# Check if analysis completed successfully
if ($LASTEXITCODE -eq 0) {
    Write-Host "`nAnalysis completed successfully! 🎉" -ForegroundColor Green
} else {
    Write-Host "`nAnalysis failed. Please check the output above. ❌" -ForegroundColor Red
}

# Deactivate virtual environment
deactivate 