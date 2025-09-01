"""
Visualization module for FX Hedging Algorithm.
Creates plots for hedge ratios, signals, and performance analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import os

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class HedgeVisualizer:
    """Handles all visualization needs for the FX hedging algorithm."""
    
    def __init__(self, output_dir: str = "plots"):
        """Initialize visualizer with output directory."""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_hedge_signals(self, results: Dict[str, Any], historical_data=None, show_plot: bool = True, save_plot: bool = True) -> str:
        """
        Create a comprehensive plot showing hedge ratio and component signals.
        
        Args:
            results: Algorithm results dictionary
            show_plot: Whether to display the plot
            save_plot: Whether to save the plot to file
            
        Returns:
            Path to saved plot file
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('FX Hedging Algorithm Analysis', fontsize=16, fontweight='bold')
        
        # Use real historical data if provided, otherwise generate demo data
        if historical_data is not None and not historical_data.empty:
            # Use last 30 days of real data
            recent_data = historical_data.tail(30).copy()
            dates = pd.to_datetime(recent_data['Date'])
            fx_rates = recent_data['MYR_USD'].values
            
            # Generate realistic signal evolution based on actual FX movements
            fx_returns = np.diff(fx_rates) / fx_rates[:-1]
            momentum_history = np.concatenate([[results.get('momentum_signal', 0.5)], 
                                             0.5 + np.cumsum(fx_returns) * 2])
            momentum_history = np.clip(momentum_history, 0, 1)
            
            carry_history = np.full(len(dates), results.get('carry_signal', 0.3))
            hedge_history = carry_history * 0.7 + momentum_history * 0.3
        else:
            # Fallback to demo data
            dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
            np.random.seed(42)
            carry_history = np.random.normal(results.get('carry_signal', 0.3), 0.1, 30)
            momentum_history = np.random.normal(results.get('momentum_signal', 0.9), 0.2, 30)
            hedge_history = carry_history * 0.7 + momentum_history * 0.3
            fx_rates = np.random.normal(results.get('current_fx_rate', 4.65), 0.1, 30)
        
        # Plot 1: Hedge Ratio Timeline
        axes[0, 0].plot(dates, hedge_history, 'b-', linewidth=2, marker='o', markersize=3)
        axes[0, 0].axhline(y=results.get('hedge_ratio', 0.6), color='red', linestyle='--', 
                          label=f"Current: {results.get('hedge_ratio', 0.6):.2%}")
        axes[0, 0].set_title('Hedge Ratio Over Time')
        axes[0, 0].set_ylabel('Hedge Ratio')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Signal Components
        x_pos = ['Carry Signal', 'Momentum Signal', 'Value Signal']
        y_values = [results.get('carry_signal', 0.3), results.get('momentum_signal', 0.9), results.get('value_signal', 0.5)]
        colors = ['lightcoral', 'skyblue', 'lightgreen']
        
        bars = axes[0, 1].bar(x_pos, y_values, color=colors, alpha=0.7, edgecolor='black')
        axes[0, 1].set_title('Current Signal Components')
        axes[0, 1].set_ylabel('Signal Strength')
        axes[0, 1].set_ylim(0, 1)
        
        # Add value labels on bars
        for bar, value in zip(bars, y_values):
            axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                           f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Plot 3: FX Rate History
        axes[1, 0].plot(dates, fx_rates, 'g-', linewidth=2, alpha=0.8)
        axes[1, 0].axhline(y=results.get('current_fx_rate', 4.65), color='red', linestyle='--',
                          label=f"Current: {results.get('current_fx_rate', 4.65):.3f}")
        axes[1, 0].set_title('MYR/USD Exchange Rate')
        axes[1, 0].set_ylabel('MYR per USD')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Risk Metrics (Demo)
        risk_metrics = ['Unhedged Risk', 'Current Hedge', 'Recommended']
        risk_values = [0.85, 0.45, 0.35]  # Sample risk values
        colors = ['red', 'orange', 'green']
        
        bars = axes[1, 1].bar(risk_metrics, risk_values, color=colors, alpha=0.7, edgecolor='black')
        axes[1, 1].set_title('Portfolio Risk Comparison')
        axes[1, 1].set_ylabel('Risk Level')
        axes[1, 1].set_ylim(0, 1)
        
        # Add value labels
        for bar, value in zip(bars, risk_values):
            axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                           f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save plot
        plot_path = ""
        if save_plot:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            plot_path = os.path.join(self.output_dir, f"hedge_analysis_{timestamp}.png")
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            print(f"📊 Plot saved to: {plot_path}")
        
        # Show plot
        if show_plot:
            plt.show()
        else:
            plt.close()
            
        return plot_path
    
    def plot_signal_history(self, days: int = 30, show_plot: bool = True) -> str:
        """
        Plot historical signal evolution.
        
        Args:
            days: Number of days to simulate
            show_plot: Whether to display the plot
            
        Returns:
            Path to saved plot file
        """
        # Generate sample data
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        np.random.seed(42)
        
        carry_signals = np.cumsum(np.random.normal(0, 0.02, days)) + 0.6
        momentum_signals = np.cumsum(np.random.normal(0, 0.03, days)) + 0.3
        value_signals = np.zeros(days)  # Value signal consistently 0 for undervalued MYR
        
        # Constrain signals to reasonable ranges
        carry_signals = np.clip(carry_signals, 0, 1)
        momentum_signals = np.clip(momentum_signals, 0, 1)
        value_signals = np.clip(value_signals, 0, 1)
        
        plt.figure(figsize=(12, 6))
        plt.plot(dates, carry_signals, label='Carry Signal', linewidth=2, alpha=0.8)
        plt.plot(dates, momentum_signals, label='Momentum Signal', linewidth=2, alpha=0.8)
        plt.plot(dates, value_signals, label='Value Signal', linewidth=2, alpha=0.8)
        
        plt.title('Signal Evolution Over Time', fontsize=14, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Signal Strength')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        # Save plot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_path = os.path.join(self.output_dir, f"signal_history_{timestamp}.png")
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"📈 Signal history plot saved to: {plot_path}")
        
        if show_plot:
            plt.show()
        else:
            plt.close()
            
        return plot_path
    
    def create_summary_report(self, results: Dict[str, Any]) -> str:
        """
        Create a text-based summary report.
        
        Args:
            results: Algorithm results dictionary
            
        Returns:
            Path to saved report file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.output_dir, f"hedge_report_{timestamp}.txt")
        
        with open(report_path, 'w') as f:
            f.write("="*50 + "\n")
            f.write("FX HEDGING ALGORITHM REPORT\n")
            f.write("="*50 + "\n\n")
            
            f.write(f"Generated: {results.get('timestamp', datetime.now().isoformat())}\n")
            f.write(f"Current MYR/USD Rate: {results.get('current_fx_rate', 'N/A')}\n")
            f.write(f"Recommended Hedge Ratio: {results.get('hedge_ratio', 0):.2%}\n")
            f.write(f"Recommendation: {results.get('recommendation', 'N/A')}\n\n")
            
            f.write("SIGNAL BREAKDOWN:\n")
            f.write("-"*20 + "\n")
            f.write(f"Carry Signal: {results.get('carry_signal', 0):.3f}\n")
            f.write(f"Momentum Signal: {results.get('momentum_signal', 0):.3f}\n")
            f.write(f"Value Signal: {results.get('value_signal', 0):.3f}\n\n")
            
            f.write("CONFIGURATION:\n")
            f.write("-"*20 + "\n")
            f.write("Signal Weights: Carry 50%, Momentum 30%, Value 20%\n")
            f.write("Review Frequency: Monthly\n")
            f.write("Risk Management Focus: Portfolio volatility reduction\n")
        
        print(f"📋 Summary report saved to: {report_path}")
        return report_path