# FX Hedging Algorithm - Backtest Analysis Guide

## Overview

The backtesting module provides historical performance analysis of different hedge ratios, helping you understand the trade-offs between cost and risk reduction.

## Running Backtests

```bash
# Activate environment
conda activate fx-hedging

# Run backtest analysis
PYTHONPATH=/path/to/fx-hedging-algorithm python src/backtest.py
```

## Backtest Scenarios

The algorithm tests 6 different hedge ratios:

| Scenario | Hedge Ratio | Strategy |
|----------|-------------|----------|
| **No Hedge** | 0% | Full market exposure |
| **Conservative** | 25% | Light protection |
| **Algorithm** | 40% | Optimal balance |
| **Moderate** | 50% | Balanced approach |
| **Aggressive** | 75% | Heavy protection |
| **Full Hedge** | 100% | Complete protection |

## Understanding Results

### Cost Analysis
- **Total Cost**: What you would have paid over the period
- **vs No Hedge**: Extra cost compared to no hedging
- **Percentage**: Cost increase/decrease vs baseline

### Risk Analysis
- **Volatility**: Daily cost variation (±MYR amount)
- **Risk Score**: Cost-effectiveness of risk reduction
- **Lower volatility** = More predictable costs

### Example Results (278-day period)

```
Scenario             Total Cost      vs No Hedge  Volatility   Risk Score
----------------------------------------------------------------------
No Hedge (0%)        MYR  3,312,755      0.0%        281   -0.000
Conservative (25%)   MYR  3,354,080      1.2%        211 -196.307
Algorithm (40%)      MYR  3,378,876      2.0%        168 -392.613
Full Hedge (100%)    MYR  3,478,057      5.0%          0    0.000
```

## Key Insights

### 1. Cost vs Protection Trade-off
- **More hedging** = Higher costs but lower volatility
- **Less hedging** = Lower costs but higher volatility
- **Algorithm balances** both factors optimally

### 2. Market Period Impact
- **MYR strengthening period**: Hedging adds costs (opportunity cost)
- **MYR weakening period**: Hedging would save money
- **Algorithm optimizes** for unknown future scenarios

### 3. Business Decision Factors

**Choose Higher Hedge Ratios If:**
- Cash flow predictability is critical
- Cannot tolerate import cost surprises
- Have limited forex expertise

**Choose Lower Hedge Ratios If:**
- Comfortable with volatility
- Believe MYR will strengthen
- Want maximum upside participation

## Generated Files

### Backtest Report (`backtest_report_YYYYMMDD_HHMMSS.txt`)
- Detailed scenario comparison
- Performance metrics
- Key insights and recommendations

### Backtest Visualization (`backtest_analysis_YYYYMMDD_HHMMSS.png`)
- Total cost comparison bar chart
- Cost vs no hedge analysis  
- Volatility comparison
- Risk-adjusted performance scores

## Interpretation Guide

### Risk-Adjusted Score
```
Score = -(Extra Cost ÷ Volatility Reduction)
```

- **Negative score**: You paid for protection
- **More negative**: Higher cost per unit of risk reduction
- **Less negative**: Better value for protection

### Volatility Reduction
```
Reduction = No Hedge Volatility - Hedge Volatility
```

- **Larger reduction**: More stable daily costs
- **Smaller reduction**: Less impact on day-to-day variation

### Practical Example
- **Algorithm scenario**: +MYR 66K cost, -113 MYR daily volatility
- **Translation**: Pay MYR 238/day for 40% smoother import costs
- **Business decision**: Is predictability worth MYR 238/day?

## Limitations

1. **Historical Analysis**: Past performance doesn't predict future results
2. **Simplified Costs**: Actual hedging costs may vary by institution
3. **Perfect Execution**: Assumes ideal hedge implementation
4. **Single Period**: Results specific to the backtested timeframe

## Using Results for Decision Making

### Step 1: Identify Your Risk Tolerance
- High: Consider 0-25% hedge ratios
- Moderate: Consider 25-50% hedge ratios  
- Low: Consider 50-100% hedge ratios

### Step 2: Evaluate Cost vs Benefit
- Compare extra costs vs volatility reduction
- Consider your business cash flow needs
- Factor in your market outlook

### Step 3: Monitor and Adjust
- Rerun backtests periodically
- Adjust hedge ratios based on changing conditions
- Use algorithm recommendation as baseline

## Advanced Usage

### Custom Parameters
Modify `backtest.py` to test:
- Different import amounts
- Longer/shorter time periods
- Custom hedge ratio scenarios
- Different hedging cost assumptions

### Integration with Business Planning
- Use volatility metrics for cash flow forecasting
- Incorporate results into annual budgeting
- Align hedge ratios with business risk appetite

## Support

For questions about backtest interpretation or customization:
1. Review the generated report files
2. Check the visualization plots
3. Refer to this guide for metric definitions
4. Consider consulting with forex specialists for complex scenarios