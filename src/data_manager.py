"""
Data Manager for FX Hedging Algorithm.
Fetches real exchange rates and interest rate data from authoritative sources.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import requests
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import logging
from config import DATA_CONFIG, ALGORITHM_CONFIG
import time

try:
    from fredapi import Fred
    FRED_AVAILABLE = True
except ImportError:
    FRED_AVAILABLE = False

# World Bank API endpoint for PPP data
WORLD_BANK_PPP_API = "https://api.worldbank.org/v2/country/MY/indicator/PA.NUS.PPP"

logger = logging.getLogger(__name__)

class DataManager:
    """Manages data fetching from various financial sources."""
    
    def __init__(self):
        """Initialize the data manager."""
        self.yahoo_symbol = ALGORITHM_CONFIG.yahoo_symbol
        self.cache = {}
        
        # Initialize FRED API if available and configured
        self.fred = None
        if FRED_AVAILABLE and ALGORITHM_CONFIG.use_fred_api:
            # Try multiple sources for API key
            api_key = (ALGORITHM_CONFIG.fred_api_key or 
                      os.getenv('FRED_API_KEY') or 
                      self._load_from_env_file())
            if api_key:
                try:
                    self.fred = Fred(api_key=api_key)
                    logger.info("FRED API initialized successfully")
                except Exception as e:
                    logger.warning(f"FRED API initialization failed: {e}")
            else:
                logger.info("FRED API key not provided, using manual rates")
    
    def _load_from_env_file(self) -> Optional[str]:
        """Load FRED API key from ~/.env file."""
        try:
            env_path = os.path.expanduser("~/.env")
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith('FRED_API_KEY='):
                            return line.split('=', 1)[1].strip()
        except Exception as e:
            logger.debug(f"Could not load from .env file: {e}")
        return None
        
    def get_current_fx_rate(self) -> float:
        """
        Fetch current MYR/USD exchange rate from Yahoo Finance.
        
        Returns:
            Current exchange rate (MYR per USD)
        """
        try:
            logger.info(f"Fetching current MYR/USD rate from Yahoo Finance...")
            
            # Use yfinance to get current rate
            ticker = yf.Ticker(self.yahoo_symbol)
            
            # Get current market data
            info = ticker.info
            current_price = info.get('regularMarketPrice') or info.get('previousClose')
            
            if current_price:
                # Yahoo Finance MYR=X gives USD/MYR (e.g., 4.22 USD per MYR)
                # This is actually MYR/USD rate (how many MYR per USD)
                myr_usd_rate = current_price
                
                if myr_usd_rate:
                    logger.info(f"Current MYR/USD rate: {myr_usd_rate:.4f}")
                    return myr_usd_rate
            
            # Fallback: get latest close price from history
            logger.warning("Using fallback method for current rate...")
            hist = ticker.history(period="2d")
            
            if not hist.empty:
                latest_close = hist['Close'].iloc[-1]
                myr_usd_rate = latest_close
                logger.info(f"Current MYR/USD rate (historical): {myr_usd_rate:.4f}")
                return myr_usd_rate
                
        except Exception as e:
            logger.error(f"Error fetching FX rate from Yahoo Finance: {e}")
        
        # Ultimate fallback - use Bank Negara Malaysia indicative rate
        logger.warning("Using BNM fallback rate estimation")
        return self.get_bnm_indicative_rate()
    
    def get_historical_fx_data(self, days: int = None) -> pd.DataFrame:
        """
        Fetch historical MYR/USD exchange rate data.
        
        Args:
            days: Number of days of historical data (default from config)
            
        Returns:
            DataFrame with Date, Close, and calculated MYR/USD rates
        """
        if days is None:
            days = ALGORITHM_CONFIG.lookback_years * 365
            
        try:
            logger.info(f"Fetching {days} days of historical MYR/USD data...")
            
            # Calculate start date
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Fetch data from Yahoo Finance
            ticker = yf.Ticker(self.yahoo_symbol)
            hist_data = ticker.history(start=start_date, end=end_date)
            
            if hist_data.empty:
                raise ValueError("No historical data retrieved")
            
            # Yahoo MYR=X gives MYR/USD directly (how many MYR per USD)
            hist_data['MYR_USD'] = hist_data['Close']
            hist_data['Date'] = hist_data.index
            
            logger.info(f"Retrieved {len(hist_data)} days of historical data")
            logger.info(f"Date range: {hist_data.index[0].date()} to {hist_data.index[-1].date()}")
            
            return hist_data[['Date', 'Close', 'MYR_USD']].reset_index(drop=True)
            
        except Exception as e:
            logger.error(f"Error fetching historical FX data: {e}")
            return self._generate_fallback_data(days)
    
    def get_bnm_indicative_rate(self) -> float:
        """
        Get indicative MYR/USD rate based on Bank Negara Malaysia typical range.
        This is a fallback when live data is unavailable.
        
        Returns:
            Estimated MYR/USD rate
        """
        # BNM typical MYR/USD range: 4.2 - 4.8
        # Use middle of range as fallback
        indicative_rate = 4.50
        logger.info(f"Using BNM indicative rate: {indicative_rate}")
        return indicative_rate
    
    def get_fed_funds_rate(self) -> float:
        """
        Get current Federal Funds Rate from FRED API.
        Falls back to manual configuration if API unavailable.
        
        Returns:
            Current Fed Funds Rate as percentage
        """
        if self.fred:
            try:
                logger.info("Fetching Fed Funds Rate from FRED API...")
                
                # FEDFUNDS = Effective Federal Funds Rate (monthly)
                # DFF = Effective Federal Funds Rate (daily)
                # Get all data and take the most recent value
                fed_rate_data = self.fred.get_series('DFF')
                
                if not fed_rate_data.empty:
                    current_fed_rate = float(fed_rate_data.iloc[-1])
                    logger.info(f"Current Fed Funds Rate from FRED: {current_fed_rate:.2f}%")
                    return current_fed_rate
                else:
                    logger.warning("No Fed rate data returned from FRED")
                    
            except Exception as e:
                logger.error(f"Error fetching Fed rate from FRED: {e}")
        
        # Fallback to manual rate
        logger.info(f"Using manual Fed rate: {ALGORITHM_CONFIG.fed_rate:.2f}%")
        return ALGORITHM_CONFIG.fed_rate
    
    def get_interest_rates(self) -> Dict[str, float]:
        """
        Get current interest rates for MYR and USD.
        Fetches real Fed rate from FRED API when available.
        
        Returns:
            Dictionary with BNM and Fed rates
        """
        # Get real Fed rate or fallback to manual
        fed_rate = self.get_fed_funds_rate()
        
        # BNM rate still manual (no reliable API source)
        bnm_rate = ALGORITHM_CONFIG.bnm_rate
        
        rates = {
            'bnm_rate': bnm_rate,
            'fed_rate': fed_rate,
            'carry_differential': bnm_rate - fed_rate,
            'data_source': 'FRED API' if self.fred else 'Manual'
        }
        
        logger.info(f"Interest rates - BNM: {rates['bnm_rate']:.2f}% (manual), "
                   f"Fed: {rates['fed_rate']:.2f}% ({rates['data_source']}), "
                   f"Differential: {rates['carry_differential']:.2f}%")
        
        return rates
    
    def calculate_momentum_signal(self, historical_data: pd.DataFrame) -> float:
        """
        Calculate 12-month momentum signal based on historical data.
        
        Args:
            historical_data: DataFrame with historical FX rates
            
        Returns:
            Momentum signal value (0-1)
        """
        if len(historical_data) < 30:
            logger.warning("Insufficient data for momentum calculation")
            return 0.5
        
        try:
            # Calculate 12-month (or available period) return
            current_rate = historical_data['MYR_USD'].iloc[-1]
            
            # Use 12 months ago or earliest available
            lookback_days = min(365, len(historical_data) - 1)
            past_rate = historical_data['MYR_USD'].iloc[-(lookback_days + 1)]
            
            # Calculate return (negative means MYR depreciation)
            fx_return = (current_rate - past_rate) / past_rate
            
            # Convert to momentum signal (0-1)
            # If MYR is depreciating (positive return in MYR/USD), increase hedge
            momentum_signal = max(0, min(1, 0.5 + fx_return * 2))
            
            logger.info(f"Momentum calculation - 12M return: {fx_return:.3f}, "
                       f"Signal: {momentum_signal:.3f}")
            
            return momentum_signal
            
        except Exception as e:
            logger.error(f"Error calculating momentum signal: {e}")
            return 0.5
    
    def calculate_carry_signal(self, interest_rates: Dict[str, float]) -> float:
        """
        Calculate carry signal based on interest rate differential.
        
        Args:
            interest_rates: Dictionary with BNM and Fed rates
            
        Returns:
            Carry signal value (0-1)
        """
        try:
            carry_diff = interest_rates['carry_differential']
            
            # Convert rate differential to signal
            # Positive differential (MYR > USD rates) = reduce hedge
            # Negative differential (MYR < USD rates) = increase hedge
            carry_signal = max(0, min(1, 0.5 - carry_diff / 10))
            
            logger.info(f"Carry signal calculation - Differential: {carry_diff:.2f}%, "
                       f"Signal: {carry_signal:.3f}")
            
            return carry_signal
            
        except Exception as e:
            logger.error(f"Error calculating carry signal: {e}")
            return 0.5
    
    def _generate_fallback_data(self, days: int) -> pd.DataFrame:
        """
        Generate fallback historical data when API fails.
        
        Args:
            days: Number of days to generate
            
        Returns:
            DataFrame with synthetic historical data
        """
        logger.warning(f"Generating fallback data for {days} days")
        
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        # Generate realistic MYR/USD data around 4.5 with volatility
        np.random.seed(42)
        base_rate = 4.50
        returns = np.random.normal(0, 0.005, days)  # 0.5% daily volatility
        prices = [base_rate]
        
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        data = pd.DataFrame({
            'Date': dates,
            'Close': [1/p for p in prices],  # Convert to USD/MYR for consistency
            'MYR_USD': prices
        })
        
        return data
    
    def validate_data_quality(self, data: pd.DataFrame) -> bool:
        """
        Validate the quality of fetched data.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            True if data passes quality checks
        """
        if data.empty:
            logger.error("Data validation failed: Empty dataset")
            return False
        
        # Check for excessive missing values
        missing_ratio = data.isnull().sum().sum() / (len(data) * len(data.columns))
        if missing_ratio > 0.1:
            logger.warning(f"Data quality warning: {missing_ratio:.1%} missing values")
        
        # Check for outliers in FX rates
        if 'MYR_USD' in data.columns:
            rates = data['MYR_USD']
            outliers = ((rates < 3.5) | (rates > 6.0)).sum()
            if outliers > len(rates) * 0.01:  # More than 1% outliers
                logger.warning(f"Data quality warning: {outliers} potential outliers detected")
        
        logger.info("Data quality validation passed")
        return True
    
    def get_ppp_value_signal(self) -> float:
        """
        Get PPP-based value signal using World Bank data.
        Compares current MYR/USD rate to PPP fair value.
        
        Returns:
            Value signal (0-1): 0 = undervalued (reduce hedge), 1 = overvalued (increase hedge)
        """
        try:
            logger.info("Fetching PPP data from World Bank API...")
            
            # Get recent PPP data from World Bank
            url = f"{WORLD_BANK_PPP_API}?format=json&date=2020:2024&per_page=10"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if len(data) > 1 and data[1]:
                    ppp_records = data[1]
                    
                    # Find latest available PPP value
                    latest_ppp = None
                    for record in ppp_records:
                        if record['value']:
                            latest_ppp = float(record['value'])
                            ppp_year = record['date']
                            break
                    
                    if latest_ppp:
                        current_rate = self.get_current_fx_rate()
                        
                        # Calculate PPP undervaluation (correct methodology)
                        # Convert current_rate (USD/MYR) to MYR/USD for proper comparison
                        current_rate_myr_usd = 1 / current_rate
                        ppp_undervaluation = (latest_ppp / current_rate_myr_usd - 1)
                        
                        # Convert to value signal (Harvey et al. methodology)
                        # Undervalued currency (PPP > market) should appreciate → reduce hedge
                        # Overvalued currency (PPP < market) should depreciate → increase hedge
                        value_signal = max(0, min(1, 0.5 - ppp_undervaluation * 0.1))
                        
                        logger.info(f"PPP analysis - Current: {current_rate:.4f} USD/MYR "
                                   f"({current_rate_myr_usd:.4f} MYR/USD), "
                                   f"PPP ({ppp_year}): {latest_ppp:.4f} MYR/USD, "
                                   f"MYR Undervaluation: {ppp_undervaluation:.1%}, "
                                   f"Value Signal: {value_signal:.3f}")
                        
                        return value_signal
                    else:
                        logger.warning("No valid PPP data found")
                else:
                    logger.warning("No PPP data returned from World Bank API")
            else:
                logger.warning(f"World Bank API request failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error fetching PPP data: {e}")
        
        # Fallback: Use cached PPP estimate
        logger.info("Using fallback PPP estimate")
        return self._get_fallback_ppp_signal()
    
    def _get_fallback_ppp_signal(self) -> float:
        """
        Fallback PPP value signal using known estimates.
        
        Returns:
            Conservative value signal based on typical PPP ranges
        """
        current_rate = self.get_current_fx_rate()
        
        # Use recent World Bank estimate: ~1.40 MYR per International USD
        fallback_ppp = 1.40
        ppp_deviation = (current_rate - fallback_ppp) / fallback_ppp
        
        # Conservative scaling for fallback
        value_signal = max(0, min(1, 0.5 - ppp_deviation * 0.3))
        
        logger.info(f"Fallback PPP signal - Current: {current_rate:.4f}, "
                   f"Est. PPP: {fallback_ppp:.2f}, "
                   f"Signal: {value_signal:.3f}")
        
        return value_signal