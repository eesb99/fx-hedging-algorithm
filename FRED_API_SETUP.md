# FRED API Setup Guide

**NOTE:** For complete installation instructions, see [INSTALLATION.md](INSTALLATION.md). This guide focuses specifically on FRED API configuration.

## Get Your Free FRED API Key

1. **Visit FRED Website**: Go to https://fred.stlouisfed.org/
2. **Create Account**: Click "Sign Up" and create a free account
3. **Request API Key**: 
   - Log in to your account
   - Go to "My Account" → "API Keys"
   - Click "Request API Key"
   - Fill out the simple form (name, email, intended use)
4. **Get Your Key**: You'll receive your API key immediately

## Configure the API Key

### Option 1: Environment File (Recommended)
```bash
# Create ~/.env file
echo "FRED_API_KEY=your_api_key_here" > ~/.env

# Alternative: Set environment variable
export FRED_API_KEY="your_api_key_here"
```

### Option 2: Configuration File
Edit `src/config.py`:
```python
fred_api_key: str = "your_api_key_here"
```

## Test the Setup

```bash
# Activate environment
conda activate fx-hedging

# Test Fed rate fetching
python -c "from src.data_manager import DataManager; dm = DataManager(); print('Fed Rate:', dm.get_fed_funds_rate())"

# Run full algorithm
python src/main.py
```

## What You Get

With FRED API enabled:
- **Real Fed Funds Rate**: Live daily updates from Federal Reserve
- **Historical Data**: Access to decades of Fed rate history
- **Authoritative Source**: Direct from St. Louis Federal Reserve Bank

## Fallback Behavior

If FRED API is unavailable:
- Uses manual Fed rate from config (currently 5.25%)
- Algorithm continues to function normally
- Log messages indicate data source used

## FRED Data Series Used

- **DFF**: Effective Federal Funds Rate (Daily)
- **FEDFUNDS**: Effective Federal Funds Rate (Monthly)

## Rate Limits

- FRED API is free with generous limits
- 120 requests per minute
- Perfect for algorithmic trading applications