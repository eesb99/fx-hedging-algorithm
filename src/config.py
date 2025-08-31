"""Configuration settings for the FX Hedging Algorithm."""

import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AlgorithmConfig:
    """Core algorithm configuration parameters."""
    
    # Signal weights (must sum to 1.0)
    carry_weight: float = 0.7
    momentum_weight: float = 0.3
    
    # Data parameters
    yahoo_symbol: str = "MYR=X"
    lookback_years: int = 2
    
    # Hedge ratio constraints
    min_hedge_ratio: float = 0.0
    max_hedge_ratio: float = 1.0
    
    # Review frequency
    rebalance_frequency: str = "monthly"  # monthly, weekly, quarterly
    
    # Interest rates (manual fallback - can be overridden by API data)
    bnm_rate: float = 3.0  # Bank Negara Malaysia rate (manual)
    fed_rate: float = 5.25  # Federal Reserve rate (manual fallback)
    
    # FRED API configuration
    fred_api_key: str = ""  # Set your FRED API key here or via environment variable
    use_fred_api: bool = True  # Enable/disable FRED API usage
    
    def __post_init__(self):
        """Validate configuration parameters."""
        if abs(self.carry_weight + self.momentum_weight - 1.0) > 1e-6:
            raise ValueError("Signal weights must sum to 1.0")
        
        if not (0.0 <= self.min_hedge_ratio <= self.max_hedge_ratio <= 1.0):
            raise ValueError("Invalid hedge ratio constraints")

@dataclass 
class DataConfig:
    """Data source and storage configuration."""
    
    # Data directories
    data_dir: str = "data"
    cache_dir: str = "data/cache"
    
    # Yahoo Finance settings
    yahoo_timeout: int = 10
    max_retries: int = 3
    
    # Data validation
    max_missing_days: int = 5
    outlier_threshold: float = 0.1  # 10% daily move threshold
    
    def __post_init__(self):
        """Create data directories if they don't exist."""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.cache_dir, exist_ok=True)

# Global configuration instances
ALGORITHM_CONFIG = AlgorithmConfig()
DATA_CONFIG = DataConfig()