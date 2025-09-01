#!/usr/bin/env python3
"""
Dynamic FX Hedging Algorithm - Main Entry Point

This script runs the complete hedging algorithm pipeline:
1. Fetch latest MYR/USD data
2. Calculate carry and momentum signals  
3. Generate hedge ratio recommendation
4. Display results and save to file
"""

import logging
from datetime import datetime
from typing import Dict, Any

from config import ALGORITHM_CONFIG, DATA_CONFIG
from visualizer import HedgeVisualizer
from data_manager import DataManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main() -> Dict[str, Any]:
    """
    Execute the complete FX hedging algorithm pipeline.
    
    Returns:
        Dict containing hedge ratio and supporting data
    """
    logger.info("Starting Dynamic FX Hedging Algorithm")
    logger.info(f"Configuration: Carry Weight={ALGORITHM_CONFIG.carry_weight}, "
                f"Momentum Weight={ALGORITHM_CONFIG.momentum_weight}, "
                f"Value Weight={ALGORITHM_CONFIG.value_weight}")
    
    try:
        # Initialize data manager
        data_manager = DataManager()
        
        # Fetch real market data
        logger.info("Fetching real-time market data...")
        current_fx_rate = data_manager.get_current_fx_rate()
        historical_data = data_manager.get_historical_fx_data()
        interest_rates = data_manager.get_interest_rates()
        
        # Validate data quality
        if not data_manager.validate_data_quality(historical_data):
            logger.warning("Data quality issues detected, proceeding with caution")
        
        # Calculate signals using real data
        carry_signal = data_manager.calculate_carry_signal(interest_rates)
        momentum_signal = data_manager.calculate_momentum_signal(historical_data)
        value_signal = data_manager.get_ppp_value_signal()
        
        # Calculate combined hedge ratio using three signals
        hedge_ratio = (carry_signal * ALGORITHM_CONFIG.carry_weight + 
                      momentum_signal * ALGORITHM_CONFIG.momentum_weight +
                      value_signal * ALGORITHM_CONFIG.value_weight)
        
        # Constrain within limits
        hedge_ratio = max(ALGORITHM_CONFIG.min_hedge_ratio, 
                         min(ALGORITHM_CONFIG.max_hedge_ratio, hedge_ratio))
        
        # Generate recommendation
        if hedge_ratio > 0.7:
            recommendation = "Significantly increase hedge position"
        elif hedge_ratio > 0.5:
            recommendation = "Increase hedge position"
        elif hedge_ratio > 0.3:
            recommendation = "Maintain moderate hedge position"
        else:
            recommendation = "Reduce hedge position"
        
        # Compile results
        results = {
            "timestamp": datetime.now().isoformat(),
            "hedge_ratio": hedge_ratio,
            "carry_signal": carry_signal,
            "momentum_signal": momentum_signal,
            "value_signal": value_signal,
            "current_fx_rate": current_fx_rate,
        
            "recommendation": recommendation,
            "interest_rates": interest_rates,
            "data_points": len(historical_data)
        }
        
        logger.info(f"Algorithm completed successfully")
        logger.info(f"Recommended Hedge Ratio: {results['hedge_ratio']:.2%}")
        logger.info(f"Carry Signal: {results['carry_signal']:.3f}")
        logger.info(f"Momentum Signal: {results['momentum_signal']:.3f}")
        logger.info(f"Value Signal: {results['value_signal']:.3f}")
        
        # Generate visualizations with real data
        logger.info("Creating visualizations...")
        visualizer = HedgeVisualizer()
        plot_path = visualizer.plot_hedge_signals(results, historical_data=historical_data, show_plot=False, save_plot=True)
        signal_plot_path = visualizer.plot_signal_history(days=30, show_plot=False)
        report_path = visualizer.create_summary_report(results)
        
        results['plot_path'] = plot_path
        results['signal_plot_path'] = signal_plot_path
        results['report_path'] = report_path
        
        return results
        
    except Exception as e:
        logger.error(f"Algorithm execution failed: {e}")
        raise

if __name__ == "__main__":
    results = main()
    print(f"\n=== FX Hedging Recommendation ===")
    print(f"Date: {results['timestamp'][:10]}")
    print(f"Current MYR/USD Rate: {results['current_fx_rate']:.4f}")
    print(f"Recommended Hedge Ratio: {results['hedge_ratio']:.2%}")
    print(f"Recommendation: {results['recommendation']}")
    print(f"\n📈 Market Data:")
    print(f"  - BNM Rate: {results['interest_rates']['bnm_rate']:.2f}% (manual)")
    print(f"  - Fed Rate: {results['interest_rates']['fed_rate']:.2f}% ({results['interest_rates']['data_source']})")
    print(f"  - Data Points: {results['data_points']} days")
    print(f"\n📊 Visualizations created:")
    print(f"  - Main plot: {results.get('plot_path', 'N/A')}")
    print(f"  - Signal history: {results.get('signal_plot_path', 'N/A')}")
    print(f"  - Report: {results.get('report_path', 'N/A')}")