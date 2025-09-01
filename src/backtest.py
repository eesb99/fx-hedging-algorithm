"""
Backtesting module for FX Hedging Algorithm.
Analyzes historical performance of different hedge ratios.
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import logging
from typing import Dict, List, Tuple
from data_manager import DataManager
from config import ALGORITHM_CONFIG

logger = logging.getLogger(__name__)

class BacktestEngine:
    """Backtesting engine for FX hedging strategies."""
    
    def __init__(self):
        """Initialize backtesting engine."""
        self.data_manager = DataManager()
        
    def run_backtest_scenarios(self, 
                             purchase_amount_myr: float = 1_000_000,
                             lookback_days: int = 365) -> Dict:
        """
        Run backtest scenarios comparing different hedge ratios.
        
        Args:
            purchase_amount_myr: Annual import amount in MYR
            lookback_days: Days to backtest
            
        Returns:
            Dictionary with backtest results
        """
        logger.info(f"Starting backtest for MYR {purchase_amount_myr:,.0f} over {lookback_days} days")
        
        # Get historical data
        historical_data = self.data_manager.get_historical_fx_data(lookback_days + 30)
        
        if len(historical_data) < lookback_days:
            logger.warning(f"Insufficient data: {len(historical_data)} days available")
            lookback_days = len(historical_data) - 1
        
        # Define hedge ratio scenarios
        hedge_scenarios = {
            'No Hedge (0%)': 0.0,
            'Conservative (25%)': 0.25, 
            'Algorithm (40%)': 0.40,
            'Moderate (50%)': 0.50,
            'Aggressive (75%)': 0.75,
            'Full Hedge (100%)': 1.0
        }
        
        results = {}
        
        for scenario_name, hedge_ratio in hedge_scenarios.items():
            scenario_result = self._simulate_scenario(
                historical_data, 
                purchase_amount_myr, 
                hedge_ratio, 
                lookback_days
            )
            scenario_result['hedge_ratio'] = hedge_ratio
            results[scenario_name] = scenario_result
            
        # Calculate performance metrics
        results = self._calculate_performance_metrics(results)
        
        logger.info("Backtest completed successfully")
        return results
    
    def _simulate_scenario(self, 
                          historical_data: pd.DataFrame,
                          purchase_amount_myr: float,
                          hedge_ratio: float,
                          lookback_days: int) -> Dict:
        """Simulate a specific hedge ratio scenario."""
        
        # Get the relevant period
        data = historical_data.tail(lookback_days + 1).copy()
        
        # Calculate daily costs in MYR
        daily_purchase = purchase_amount_myr / 365  # Assume even distribution
        
        costs = []
        hedge_costs = []
        total_costs = []
        
        initial_rate = data['MYR_USD'].iloc[0]
        
        for i in range(1, len(data)):
            current_rate = data['MYR_USD'].iloc[i]
            
            # Unhedged portion cost
            unhedged_cost = daily_purchase * (1 - hedge_ratio) * current_rate
            
            # Hedged portion cost (locked at initial rate)
            hedged_cost = daily_purchase * hedge_ratio * initial_rate
            
            # Hedging cost (spread/premium - simplified as 0.5% annually)
            hedge_fee = daily_purchase * hedge_ratio * 0.005 / 365
            
            total_daily_cost = unhedged_cost + hedged_cost + hedge_fee
            
            costs.append(unhedged_cost + hedged_cost)
            hedge_costs.append(hedge_fee)
            total_costs.append(total_daily_cost)
        
        return {
            'total_cost': sum(total_costs),
            'base_cost': sum(costs),
            'hedge_fees': sum(hedge_costs),
            'daily_costs': total_costs,
            'volatility': np.std(total_costs),
            'max_daily_cost': max(total_costs),
            'min_daily_cost': min(total_costs)
        }
    
    def _calculate_performance_metrics(self, results: Dict) -> Dict:
        """Calculate comparative performance metrics."""
        
        # Base comparison: No hedge scenario
        no_hedge_cost = results['No Hedge (0%)']['total_cost']
        
        for scenario_name, result in results.items():
            # Cost vs no hedge
            result['cost_vs_no_hedge'] = result['total_cost'] - no_hedge_cost
            result['cost_vs_no_hedge_pct'] = (result['total_cost'] / no_hedge_cost - 1) * 100
            
            # Risk-adjusted return (simplified Sharpe-like ratio)
            if result['volatility'] > 0:
                result['risk_adjusted_score'] = -result['cost_vs_no_hedge'] / result['volatility']
            else:
                result['risk_adjusted_score'] = 0
        
        return results
    
    def generate_backtest_report(self, 
                               results: Dict,
                               purchase_amount_myr: float) -> str:
        """Generate comprehensive backtest report."""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"plots/backtest_report_{timestamp}.txt"
        
        with open(report_path, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("FX HEDGING BACKTEST ANALYSIS REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"Import Amount: MYR {purchase_amount_myr:,.0f} annually\n")
            f.write(f"Backtest Period: {len(list(results.values())[0]['daily_costs'])} days\n\n")
            
            # Scenario comparison
            f.write("SCENARIO PERFORMANCE COMPARISON:\n")
            f.write("-" * 40 + "\n")
            f.write(f"{'Scenario':<20} {'Total Cost':<15} {'vs No Hedge':<12} {'Volatility':<12} {'Risk Score':<10}\n")
            f.write("-" * 70 + "\n")
            
            # Sort by risk-adjusted score
            sorted_scenarios = sorted(results.items(), 
                                    key=lambda x: x[1]['risk_adjusted_score'], 
                                    reverse=True)
            
            for scenario_name, result in sorted_scenarios:
                f.write(f"{scenario_name:<20} "
                       f"MYR {result['total_cost']:>10,.0f} "
                       f"{result['cost_vs_no_hedge_pct']:>8.1f}% "
                       f"{result['volatility']:>10.0f} "
                       f"{result['risk_adjusted_score']:>8.3f}\n")
            
            f.write("\n" + "DETAILED ANALYSIS:\n")
            f.write("-" * 20 + "\n")
            
            # Algorithm performance
            algo_result = results['Algorithm (40%)']
            f.write(f"Algorithm Recommendation (40% hedge):\n")
            f.write(f"  Total Cost: MYR {algo_result['total_cost']:,.0f}\n")
            f.write(f"  Cost vs No Hedge: MYR {algo_result['cost_vs_no_hedge']:+,.0f} ({algo_result['cost_vs_no_hedge_pct']:+.1f}%)\n")
            f.write(f"  Daily Volatility: MYR {algo_result['volatility']:,.0f}\n")
            f.write(f"  Risk-Adjusted Score: {algo_result['risk_adjusted_score']:.3f}\n\n")
            
            # Best performing scenario
            best_scenario = sorted_scenarios[0]
            f.write(f"Best Risk-Adjusted Performance: {best_scenario[0]}\n")
            f.write(f"  Risk Score: {best_scenario[1]['risk_adjusted_score']:.3f}\n\n")
            
            f.write("KEY INSIGHTS:\n")
            f.write("-" * 12 + "\n")
            f.write("• Higher hedge ratios reduce volatility but may increase total costs\n")
            f.write("• Algorithm balances cost efficiency with risk management\n")
            f.write("• Risk-adjusted score considers both cost impact and volatility\n")
            f.write("• Actual performance depends on specific market conditions during period\n")
        
        print(f"📊 Backtest report saved to: {report_path}")
        return report_path
    
    def plot_backtest_results(self, results: Dict) -> str:
        """Create visualization of backtest results."""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        scenarios = list(results.keys())
        colors = plt.cm.Set3(np.linspace(0, 1, len(scenarios)))
        
        # 1. Total Cost Comparison
        total_costs = [results[s]['total_cost'] for s in scenarios]
        bars1 = ax1.bar(range(len(scenarios)), total_costs, color=colors)
        ax1.set_title('Total Cost by Hedge Scenario', fontweight='bold')
        ax1.set_ylabel('Total Cost (MYR)')
        ax1.set_xticks(range(len(scenarios)))
        ax1.set_xticklabels([s.split('(')[0].strip() for s in scenarios], rotation=45)
        
        # Add value labels on bars
        for bar, cost in zip(bars1, total_costs):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(total_costs)*0.01,
                    f'MYR {cost:,.0f}', ha='center', va='bottom', fontsize=9)
        
        # 2. Cost vs No Hedge
        cost_diff = [results[s]['cost_vs_no_hedge'] for s in scenarios]
        bars2 = ax2.bar(range(len(scenarios)), cost_diff, color=colors)
        ax2.set_title('Cost Difference vs No Hedge', fontweight='bold')
        ax2.set_ylabel('Cost Difference (MYR)')
        ax2.set_xticks(range(len(scenarios)))
        ax2.set_xticklabels([s.split('(')[0].strip() for s in scenarios], rotation=45)
        ax2.axhline(y=0, color='red', linestyle='--', alpha=0.7)
        
        # 3. Volatility Comparison
        volatilities = [results[s]['volatility'] for s in scenarios]
        bars3 = ax3.bar(range(len(scenarios)), volatilities, color=colors)
        ax3.set_title('Daily Cost Volatility', fontweight='bold')
        ax3.set_ylabel('Volatility (MYR)')
        ax3.set_xticks(range(len(scenarios)))
        ax3.set_xticklabels([s.split('(')[0].strip() for s in scenarios], rotation=45)
        
        # 4. Risk-Adjusted Score
        risk_scores = [results[s]['risk_adjusted_score'] for s in scenarios]
        bars4 = ax4.bar(range(len(scenarios)), risk_scores, color=colors)
        ax4.set_title('Risk-Adjusted Performance Score', fontweight='bold')
        ax4.set_ylabel('Score (Higher = Better)')
        ax4.set_xticks(range(len(scenarios)))
        ax4.set_xticklabels([s.split('(')[0].strip() for s in scenarios], rotation=45)
        ax4.axhline(y=0, color='red', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        # Save plot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_path = f"plots/backtest_analysis_{timestamp}.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"📈 Backtest visualization saved to: {plot_path}")
        plt.close()
        
        return plot_path

def main():
    """Run backtest analysis."""
    engine = BacktestEngine()
    
    # Run backtest scenarios
    results = engine.run_backtest_scenarios(
        purchase_amount_myr=1_000_000,
        lookback_days=365
    )
    
    # Generate report and visualization
    report_path = engine.generate_backtest_report(results, 1_000_000)
    plot_path = engine.plot_backtest_results(results)
    
    # Print summary
    print("\n=== BACKTEST SUMMARY ===")
    algo_result = results['Algorithm (40%)']
    print(f"Algorithm Performance (40% hedge):")
    print(f"  Cost vs No Hedge: MYR {algo_result['cost_vs_no_hedge']:+,.0f}")
    print(f"  Risk-Adjusted Score: {algo_result['risk_adjusted_score']:.3f}")
    
    return results

if __name__ == "__main__":
    main()