# Dynamic FX Hedging Algorithm (MYR/USD)

A sophisticated currency risk management system that provides dynamic hedging recommendations for MYR/USD exposures using carry and momentum signals. **Based on Harvey et al. (2025) academic research.**

## ✅ Current Status: OPERATIONAL

**Live Algorithm**: Generates real-time hedge ratios using authoritative data sources
**Academic Validation**: Methodology confirmed against leading financial research
**Business Ready**: Tested for Malaysian importer with MYR 1M annual exposure

## Key Features

- **✅ Live Data Integration**: Yahoo Finance (FX rates) + FRED API (Fed rates)
- **✅ Dynamic Hedge Ratios**: Calculates optimal ratios (0-1) based on market signals
- **✅ Academic Methodology**: Implements Harvey et al. (2025) research findings
- **✅ Real-Time Analysis**: Current recommendation: 52.9% hedge ratio
- **✅ Comprehensive Visualization**: 4-panel analysis plots + signal history

## Quick Start

```bash
# Activate conda environment
conda activate fx-hedging

# Run the algorithm with live data
python src/main.py

# View generated plots and reports
open plots/hedge_analysis_*.png
```

## Current Market Analysis (2025-08-31)

- **MYR/USD Rate**: 4.2220 (Yahoo Finance)
- **Fed Rate**: 4.33% (FRED API)
- **BNM Rate**: 3.00% (manual)
- **Carry Signal**: 0.725 (negative carry environment)
- **Momentum Signal**: 0.286 (MYR strengthened 10.68% over 12M)
- **Recommended Hedge**: 52.9%

## Business Application

**For Malaysian Importers (MYR 1M annual purchases):**
- **Hedge Amount**: MYR 529,000 annually
- **Annual Cost**: MYR 7,036 (0.70% of purchases)
- **Monthly Implementation**: Hedge MYR 44,083/month
- **Protection**: Limits cost increases from MYR weakening

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
├── src/                 # Core algorithm (operational)
│   ├── main.py         # Main algorithm entry point
│   ├── data_manager.py # Live data fetching (Yahoo + FRED)
│   ├── config.py       # Configuration parameters
│   └── visualizer.py   # Plot generation system
├── plots/              # Generated analysis plots
├── docs/               # Research paper + setup guides
├── context/            # Project documentation
└── FRED_API_SETUP.md   # API configuration guide
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

### Disclaimer
This implementation is for educational and risk management purposes. Users should consult with financial professionals before making investment decisions. The algorithm provides analytical insights but does not constitute financial advice.