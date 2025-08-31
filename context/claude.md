# Dynamic FX Hedging Algorithm Project Context

**Project Type:** Standard (1-4 weeks)  
**Start Date:** 2025-08-31  
**Status:** Phase 1 Complete - Core Algorithm Operational  
**Last Updated:** 2025-08-31

## Project Overview
Successfully built a dynamic FX hedging algorithm for MYR/USD currency risk management using live financial data and dynamic signals (carry, momentum). Based on Harvey et al. (2025) academic research.

## Key Requirements from PRD ✅ DELIVERED
- **Target Users:** Asset managers, Malaysian exporters/importers, financial institutions
- **Core Functionality:** ✅ Dynamic hedge ratio calculation (0-1) based on carry and momentum signals
- **Data Sources:** ✅ Yahoo Finance (MYR/USD rates), ✅ FRED API (Fed rates), Manual BNM rates
- **Architecture:** ✅ Python backend, ✅ Visualization system, Jupyter notebooks ready

## Current Phase: CORE ALGORITHM COMPLETE
- ✅ Real-time data integration operational
- ✅ Live hedge ratio calculations working
- ✅ Academic methodology validated
- ✅ Business application tested (Malaysian importer scenario)

## Technical Stack - IMPLEMENTED
- **Backend:** Python 3.10 in conda environment (fx-hedging)
- **Data APIs:** Yahoo Finance (live FX), FRED API (Fed rates), Manual BNM input
- **Visualization:** matplotlib, seaborn, plotly with automated plot generation
- **Environment:** Fully isolated conda env with all dependencies

## Project Milestones - CURRENT STATUS
1. ✅ Project structure setup
2. ✅ Data Collection Module (Yahoo Finance + FRED API integration)
3. ✅ Signal & Decision Logic Module (Carry + Momentum operational)
4. ⏳ Backtest & Analytics (Next phase)
5. ⏳ Reporting/Dashboard (Basic visualization complete)
6. ✅ Live Decision Output (52.9% hedge ratio for MYR 1M importer)

## Real-World Application Validated
- **User Profile:** Malaysian importer, MYR 1M annual purchases
- **Current Recommendation:** 52.9% hedge ratio
- **Market Conditions:** BNM 3.00%, Fed 4.33% (FRED API), MYR/USD 4.2220
- **Business Impact:** Hedge MYR 529K annually, cost MYR 7,036/year
- **Fed Rate Sensitivity:** 0.25% cut → 51.1% hedge ratio

## Academic Foundation
- **Research Base:** Harvey et al. (2025) "The Best Strategies for FX Hedging"
- **Methodology:** Validated carry + momentum signals
- **Implementation:** Follows academic best practices for dynamic hedging