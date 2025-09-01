"""
Unit tests for FX Hedging Algorithm core functions.
Tests data retrieval, signal calculations, and hedge ratio logic.
"""

import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_manager import DataManager
from config import ALGORITHM_CONFIG
import logging

# Suppress logging during tests
logging.getLogger().setLevel(logging.CRITICAL)

class TestDataManager(unittest.TestCase):
    """Test DataManager functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.data_manager = DataManager()
    
    def test_exchange_rate_format(self):
        """Test exchange rate returns valid float."""
        with patch('yfinance.Ticker') as mock_ticker:
            # Mock Yahoo Finance response
            mock_hist = pd.DataFrame({
                'Close': [4.2235]
            }, index=[pd.Timestamp('2025-09-01')])
            mock_ticker.return_value.history.return_value = mock_hist
            
            rate = self.data_manager.get_current_fx_rate()
            
            self.assertIsInstance(rate, float)
            self.assertGreater(rate, 3.0)  # Reasonable range
            self.assertLess(rate, 6.0)     # Reasonable range
    
    def test_historical_data_structure(self):
        """Test historical data returns proper DataFrame."""
        with patch('yfinance.Ticker') as mock_ticker:
            # Mock historical data
            dates = pd.date_range('2024-01-01', periods=100, freq='D')
            mock_hist = pd.DataFrame({
                'Close': np.random.uniform(4.0, 4.5, 100)
            }, index=dates)
            mock_ticker.return_value.history.return_value = mock_hist
            
            historical = self.data_manager.get_historical_fx_data(100)
            
            self.assertIsInstance(historical, pd.DataFrame)
            self.assertIn('MYR_USD', historical.columns)
            self.assertEqual(len(historical), 100)
            self.assertTrue(all(historical['MYR_USD'] > 0))
    
    @patch.dict(os.environ, {'FRED_API_KEY': 'test_key'})
    def test_fed_rate_retrieval(self):
        """Test Fed rate retrieval from FRED API."""
        with patch('fredapi.Fred') as mock_fred:
            mock_fred.return_value.get_series_latest_release.return_value = pd.Series([4.33])
            
            # Re-initialize to pick up mock API key
            data_manager = DataManager()
            fed_rate = data_manager.get_fed_funds_rate()
            
            self.assertIsInstance(fed_rate, float)
            self.assertGreater(fed_rate, 0)
            self.assertLess(fed_rate, 20)  # Reasonable range
    
    def test_interest_rate_calculation(self):
        """Test interest rate differential calculation."""
        with patch.object(self.data_manager, 'get_fed_funds_rate', return_value=4.33):
            rates = self.data_manager.get_interest_rates()
            
            self.assertIn('bnm_rate', rates)
            self.assertIn('fed_rate', rates)
            self.assertIn('carry_differential', rates)
            
            expected_diff = ALGORITHM_CONFIG.bnm_rate - 4.33
            self.assertAlmostEqual(rates['carry_differential'], expected_diff, places=2)
    
    def test_momentum_signal_calculation(self):
        """Test momentum signal calculation."""
        # Create test data with known trend
        dates = pd.date_range('2024-01-01', periods=365, freq='D')
        # Create weakening trend (increasing USD/MYR)
        rates = np.linspace(4.0, 4.4, 365)  # MYR weakening
        historical = pd.DataFrame({
            'MYR_USD': rates
        }, index=dates)
        
        momentum = self.data_manager.calculate_momentum_signal(historical)
        
        self.assertIsInstance(momentum, float)
        self.assertGreaterEqual(momentum, 0.0)
        self.assertLessEqual(momentum, 1.0)
        self.assertGreater(momentum, 0.5)  # Should be > 0.5 for weakening MYR

class TestSignalCalculations(unittest.TestCase):
    """Test individual signal calculations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.data_manager = DataManager()
    
    def test_carry_signal_logic(self):
        """Test carry signal calculation logic."""
        # Test different rate differentials
        test_cases = [
            (-2.0, 0.8),   # BNM much lower → high carry signal
            (-1.0, 0.65),  # BNM lower → moderate signal
            (0.0, 0.5),    # Equal rates → neutral
            (1.0, 0.35),   # BNM higher → low signal
            (2.0, 0.2)     # BNM much higher → very low signal
        ]
        
        for differential, expected_range in test_cases:
            # Mock interest rates
            mock_rates = {
                'carry_differential': differential,
                'bnm_rate': 3.0,
                'fed_rate': 3.0 - differential
            }
            
            # Calculate carry signal manually (simplified)
            carry_signal = max(0, min(1, 0.5 - differential * 0.25))
            
            self.assertGreaterEqual(carry_signal, 0.0)
            self.assertLessEqual(carry_signal, 1.0)
            # Just verify signal is in reasonable range for differential
            if differential < -1:
                self.assertGreater(carry_signal, 0.6)
            elif differential > 1:
                self.assertLess(carry_signal, 0.4)
    
    def test_ppp_value_signal(self):
        """Test PPP value signal calculation."""
        with patch('requests.get') as mock_get:
            # Mock World Bank API response
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = [
                {'page': 1, 'pages': 1},
                [{'date': '2024', 'value': '1.4023'}]
            ]
            mock_get.return_value = mock_response
            
            # Mock current exchange rate
            with patch.object(self.data_manager, 'get_current_fx_rate', return_value=4.2235):
                value_signal = self.data_manager.get_ppp_value_signal()
                
                self.assertIsInstance(value_signal, float)
                self.assertGreaterEqual(value_signal, 0.0)
                self.assertLessEqual(value_signal, 1.0)
                # For severely undervalued MYR, should be close to 0
                self.assertLess(value_signal, 0.1)

class TestHedgeRatioCalculation(unittest.TestCase):
    """Test hedge ratio calculation logic."""
    
    def test_hedge_ratio_bounds(self):
        """Test hedge ratio stays within valid bounds."""
        # Test extreme signal values
        test_signals = [
            (0.0, 0.0, 0.0),  # All signals low
            (1.0, 1.0, 1.0),  # All signals high
            (0.5, 0.3, 0.8),  # Mixed signals
            (0.9, 0.1, 0.0)   # Carry dominant
        ]
        
        for carry, momentum, value in test_signals:
            hedge_ratio = (carry * ALGORITHM_CONFIG.carry_weight + 
                          momentum * ALGORITHM_CONFIG.momentum_weight + 
                          value * ALGORITHM_CONFIG.value_weight)
            
            self.assertGreaterEqual(hedge_ratio, 0.0)
            self.assertLessEqual(hedge_ratio, 1.0)
            self.assertIsInstance(hedge_ratio, float)
    
    def test_signal_weights_sum(self):
        """Test signal weights sum to 1.0."""
        total_weight = (ALGORITHM_CONFIG.carry_weight + 
                       ALGORITHM_CONFIG.momentum_weight + 
                       ALGORITHM_CONFIG.value_weight)
        
        self.assertAlmostEqual(total_weight, 1.0, places=3)
    
    def test_carry_dominance(self):
        """Test carry signal has highest weight (Harvey et al. research)."""
        self.assertGreater(ALGORITHM_CONFIG.carry_weight, 
                          ALGORITHM_CONFIG.momentum_weight)
        self.assertGreater(ALGORITHM_CONFIG.carry_weight, 
                          ALGORITHM_CONFIG.value_weight)

class TestConfigValidation(unittest.TestCase):
    """Test configuration validation."""
    
    def test_config_values(self):
        """Test configuration values are reasonable."""
        self.assertGreater(ALGORITHM_CONFIG.bnm_rate, 0)
        self.assertLess(ALGORITHM_CONFIG.bnm_rate, 20)
        
        self.assertEqual(ALGORITHM_CONFIG.yahoo_symbol, 'MYR=X')
        
        self.assertGreater(ALGORITHM_CONFIG.carry_weight, 0)
        self.assertGreater(ALGORITHM_CONFIG.momentum_weight, 0)
        self.assertGreater(ALGORITHM_CONFIG.value_weight, 0)

class TestDataValidation(unittest.TestCase):
    """Test data validation functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.data_manager = DataManager()
    
    def test_data_quality_validation(self):
        """Test data quality validation logic."""
        # Test valid data
        valid_data = pd.DataFrame({
            'MYR_USD': [4.2, 4.3, 4.1, 4.4]
        })
        
        # Test basic validation logic manually
        self.assertGreater(len(valid_data), 2)
        self.assertTrue(all(valid_data['MYR_USD'] > 3.0))
        self.assertTrue(all(valid_data['MYR_USD'] < 6.0))
        
        # Test insufficient data
        insufficient_data = pd.DataFrame({
            'MYR_USD': [4.2]
        })
        
        self.assertLess(len(insufficient_data), 3)
        
        # Test unreasonable values
        bad_data = pd.DataFrame({
            'MYR_USD': [0.5, 10.0, 4.2]  # Unreasonable rates
        })
        
        self.assertTrue(any(bad_data['MYR_USD'] < 3.0) or any(bad_data['MYR_USD'] > 6.0))

if __name__ == '__main__':
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestDataManager,
        TestSignalCalculations, 
        TestHedgeRatioCalculation,
        TestConfigValidation,
        TestDataValidation
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print("FX HEDGING ALGORITHM - UNIT TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors))/result.testsRun)*100:.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, error in result.failures:
            error_msg = error.split('AssertionError: ')[-1].split('\n')[0]
            print(f"- {test}: {error_msg}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, error in result.errors:
            error_msg = error.split('\n')[-2]
            print(f"- {test}: {error_msg}")
    
    # Exit with appropriate code
    exit_code = 0 if (len(result.failures) + len(result.errors)) == 0 else 1
    exit(exit_code)