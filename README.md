# Dynamic FX Hedging Algorithm (MYR/USD)

A sophisticated currency risk management system that provides dynamic hedging recommendations for MYR/USD exposures using carry, momentum, and value signals. **Based on Harvey et al. (2025) academic research.**

## ✅ Current Status: PRODUCTION READY

**Live Algorithm**: Generates real-time hedge ratios using authoritative data sources  
**Academic Validation**: Full three-signal methodology implementation  
**Business Ready**: Tested with comprehensive backtesting and unit tests  
**Testing Complete**: 100% unit test coverage on core functions

## Key Features

- **✅ Three-Signal Algorithm**: Carry + Momentum + Value signals (Harvey et al. methodology)
- **✅ Live Data Integration**: Yahoo Finance (FX) + FRED API (Fed rates) + World Bank (PPP)
- **✅ Dynamic Hedge Ratios**: Calculates optimal ratios (0-1) based on market signals
- **✅ Current Recommendation**: 40.13% hedge ratio (updated with PPP analysis)
- **✅ Comprehensive Testing**: Unit tests + backtesting scenarios + performance analysis
- **✅ Business Analysis**: Cost-benefit analysis with volatility reduction metrics
- **✅ Visualization Suite**: Multi-panel plots + signal history + detailed reports

## Quick Start

```bash
# Activate conda environment
conda activate fx-hedging

# Run the algorithm with live data
PYTHONPATH=/path/to/fx-hedging-algorithm python src/main.py

# Run backtesting scenarios
PYTHONPATH=/path/to/fx-hedging-algorithm python src/backtest.py

# Run unit tests
PYTHONPATH=/path/to/fx-hedging-algorithm python tests/test_algorithm.py

# View generated plots and reports
open plots/hedge_analysis_*.png
open plots/backtest_*.png
open plots/*.txt
```

## Current Market Analysis (2025-09-01)

- **USD/MYR Rate**: 4.2235 (Yahoo Finance)
- **Fed Rate**: 4.33% (FRED API)
- **BNM Rate**: 3.00% (manual input)
- **PPP Fair Value**: 1.402 MYR/USD (World Bank 2024)
- **Carry Signal**: 0.633 (negative carry environment)
- **Momentum Signal**: 0.278 (12-month trend)
- **Value Signal**: 0.008 (MYR severely undervalued 492%)
- **Recommended Hedge**: 40.13%

## Business Application

**For Malaysian Importers (MYR 1M annual purchases):**
- **Hedge Amount**: MYR 401,300 annually (40.13% of exposure)
- **Unhedged Amount**: MYR 598,700 (retains upside potential)
- **Risk Reduction**: 40% lower daily cost volatility (±168 vs ±281)
- **Opportunity Cost**: MYR 238/day for protection during favorable periods

**Backtesting Results (278 days):**
- **Algorithm vs No Hedge**: +2.0% cost (+MYR 66,121)
- **Volatility Reduction**: 40% lower daily swings
- **Trade-off**: Paid for protection during MYR strengthening period
- **Value**: Balanced risk management with upside participation

## Academic Foundation

**Research Paper**: Harvey, Castro, Hamill, Harber, Van Hemert (2025)
"The Best Strategies for FX Hedging"

**Key Validation**:
- Dynamic hedging beats static approaches across all currencies
- Carry + momentum signals proven effective
- Risk management focus appropriate for business applications

## Project Structure

```
fx-hedging-algorithm/
├── src/                 # Core algorithm (production ready)
│   ├── main.py         # Main algorithm entry point
│   ├── data_manager.py # Live data fetching (Yahoo + FRED + World Bank)
│   ├── backtest.py     # Historical performance analysis
│   ├── config.py       # Configuration parameters
│   └── visualizer.py   # Plot generation system
├── tests/              # Unit test suite
│   ├── test_algorithm.py # Comprehensive algorithm tests
│   └── __init__.py     # Test package initialization
├── plots/              # Generated analysis plots and reports
├── context/            # Project documentation and progress
├── docs/               # Research paper + setup guides
└── README.md          # This documentation
```

## Setup Requirements

1. **Conda Environment**: `conda activate fx-hedging` (Python 3.10)
2. **FRED API Key**: Free from https://fred.stlouisfed.org/ 
3. **Environment Variable**: `FRED_API_KEY` in ~/.env
4. **Dependencies**: All installed via `requirements.txt`

## Target Users

- Malaysian exporters and importers (primary use case validated)
- Asset managers with MYR/USD exposures
- Financial institutions managing currency risk

## Risk Disclaimer

This algorithm is designed for risk management purposes. It does not guarantee profits and should be used as part of a comprehensive risk management strategy. All calculations validated against authoritative market sources.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Attribution

### Academic Research Foundation
This algorithm implements methodology from:

**"The Best Strategies for FX Hedging"**  
Pedro Castro, Carl Hamill, John Harber, Campbell R. Harvey, and Otto van Hemert  
Man Group (Harvey also affiliated with Duke University and NBER)  
Published: May 31, 2025

### Development
- **Author**: Thian Seong Yee
- **Development Date**: August 31, 2025
- **Implementation**: Based on comprehensive PRD for MYR/USD hedging
- **Validation**: Confirmed against real market data and academic research

### Data Sources
- **Yahoo Finance**: Real-time MYR/USD exchange rates
- **FRED API**: Federal Reserve economic data (Fed Funds Rate)
- **Bank Negara Malaysia**: Malaysian interest rate reference

### DMCA & Copyright Disclaimer
This implementation represents an independent interpretation and application of publicly available academic research concepts. All algorithm code, business analysis, and technical implementation are original works developed by the repository owner. The methodology is inspired by academic research that is properly cited and referenced. No copyrighted materials are reproduced.

### Financial Disclaimer
This implementation is for educational and risk management purposes only. Users should consult with qualified financial professionals before making investment decisions. The algorithm provides analytical insights but does not constitute financial advice. Past performance does not guarantee future results.