# FX Hedging Algorithm - Installation & Setup Guide

## Prerequisites

- **Python 3.10+** (recommended via Anaconda/Miniconda)
- **FRED API Key** (free from Federal Reserve)
- **Internet connection** for live data feeds

## Quick Installation

### 1. Clone Repository
```bash
git clone https://github.com/eesb99/fx-hedging-algorithm.git
cd fx-hedging-algorithm
```

### 2. Create Conda Environment
```bash
# Create environment with Python 3.10
conda create -n fx-hedging python=3.10

# Activate environment
conda activate fx-hedging
```

### 3. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

### 4. Get FRED API Key
1. Visit https://fred.stlouisfed.org/
2. Create free account
3. Go to "My Account" → "API Keys"
4. Generate new API key

### 5. Configure Environment
```bash
# Create environment file
echo "FRED_API_KEY=your_api_key_here" > ~/.env

# Replace 'your_api_key_here' with actual key
```

### 6. Test Installation
```bash
# Run algorithm test
PYTHONPATH=/path/to/fx-hedging-algorithm python src/main.py

# Run unit tests
PYTHONPATH=/path/to/fx-hedging-algorithm python tests/test_algorithm.py
```

## Manual Setup (Alternative)

### Python Dependencies
```bash
pip install pandas numpy yfinance matplotlib seaborn plotly fredapi requests python-dotenv
```

### Package Versions (Tested)
```
pandas>=2.0.0
numpy>=1.24.0
yfinance>=0.2.18
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.17.0
fredapi>=0.5.1
requests>=2.31.0
python-dotenv>=1.0.0
```

## Configuration Files

### Environment Variables (.env)
Create `~/.env` file:
```bash
# Required: FRED API for Fed rates
FRED_API_KEY=your_fred_api_key

# Optional: Custom configurations
BNM_RATE=3.00
YAHOO_SYMBOL=MYR=X
```

### Algorithm Configuration
Edit `src/config.py` for:
- Signal weights (carry/momentum/value)
- Interest rate settings
- Data source parameters

## Directory Structure After Setup

```
fx-hedging-algorithm/
├── src/                 # Source code
├── tests/              # Unit tests
├── plots/              # Generated outputs
├── context/            # Documentation
├── requirements.txt    # Dependencies
├── README.md          # Main documentation
├── INSTALLATION.md    # This guide
└── BACKTEST_GUIDE.md  # Backtest documentation
```

## Verification Steps

### 1. Basic Algorithm Run
```bash
cd fx-hedging-algorithm
PYTHONPATH=$(pwd) python src/main.py
```

Expected output:
```
=== FX Hedging Recommendation ===
Date: 2025-09-01
Current MYR/USD Rate: 4.xxxx
Recommended Hedge Ratio: xx.xx%
```

### 2. Unit Tests
```bash
PYTHONPATH=$(pwd) python tests/test_algorithm.py
```

Expected output:
```
Tests Run: 12
Failures: 0
Errors: 0
Success Rate: 100.0%
```

### 3. Backtest Analysis
```bash
PYTHONPATH=$(pwd) python src/backtest.py
```

Expected outputs:
- `plots/backtest_report_*.txt`
- `plots/backtest_analysis_*.png`

## Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Solution: Set PYTHONPATH
export PYTHONPATH=/full/path/to/fx-hedging-algorithm
```

**2. FRED API Errors**
```bash
# Check API key
echo $FRED_API_KEY

# Verify .env file
cat ~/.env
```

**3. Yahoo Finance Timeouts**
- Retry after a few minutes
- Check internet connection
- Yahoo Finance occasionally rate limits

**4. Conda Environment Issues**
```bash
# Recreate environment
conda deactivate
conda remove -n fx-hedging --all
conda create -n fx-hedging python=3.10
conda activate fx-hedging
pip install -r requirements.txt
```

### Data Source Validation

**Test Yahoo Finance Connection:**
```python
import yfinance as yf
ticker = yf.Ticker("MYR=X")
print(ticker.history(period="1d"))
```

**Test FRED API Connection:**
```python
from fredapi import Fred
import os
fred = Fred(api_key=os.getenv('FRED_API_KEY'))
print(fred.get_series_latest_release('FEDFUNDS'))
```

**Test World Bank API:**
```python
import requests
url = "https://api.worldbank.org/v2/country/MYS/indicator/PA.NUS.PPP?format=json&date=2024"
response = requests.get(url)
print(response.status_code)
```

## Performance Optimization

### For Faster Execution
```bash
# Use specific Python path
/opt/miniconda3/envs/fx-hedging/bin/python src/main.py

# Reduce historical data period in config.py
DEFAULT_LOOKBACK_DAYS = 365  # Instead of 730
```

### For Development
```bash
# Install development dependencies
pip install jupyter ipython pytest

# Launch Jupyter for analysis
jupyter lab
```

## Usage Patterns

### Daily Production Use
```bash
#!/bin/bash
# daily_hedge_update.sh
cd /path/to/fx-hedging-algorithm
conda activate fx-hedging
PYTHONPATH=$(pwd) python src/main.py > daily_output.log 2>&1
```

### Weekly Analysis
```bash
#!/bin/bash
# weekly_backtest.sh
cd /path/to/fx-hedging-algorithm
conda activate fx-hedging
PYTHONPATH=$(pwd) python src/backtest.py
```

## Security Considerations

1. **Keep API keys secure** - Never commit to version control
2. **Use environment variables** - Store sensitive data in `~/.env`
3. **Regular updates** - Keep dependencies updated for security patches
4. **Access controls** - Limit access to production environment

## Support & Updates

### Getting Help
1. Check this installation guide
2. Review error messages carefully
3. Verify API key configurations
4. Test individual components

### Updating
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run tests
PYTHONPATH=$(pwd) python tests/test_algorithm.py
```

### Monitoring
- Watch for API rate limits
- Monitor data quality in logs
- Check output files for consistency
- Validate against external sources periodically

## License & Attribution

This software is provided under MIT License. See [README.md](README.md) for full attribution and academic research citations.