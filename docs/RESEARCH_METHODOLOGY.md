# Research Methodology & Academic Foundation

## Academic Research Basis

This algorithm is **inspired by** and implements methodology concepts from:

**"The Best Strategies for FX Hedging"**  
Authors: Pedro Castro, Carl Hamill, John Harber, Campbell R. Harvey, and Otto van Hemert  
Affiliation: Man Group (Harvey also affiliated with Duke University and NBER)  
Publication Date: May 31, 2025  
Available at: [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5047797)

## Key Research Findings Applied

### 1. Dynamic vs Static Hedging
**Research Finding**: Dynamic hedging strategies consistently outperform static approaches (0% or 100% hedging) across multiple currency pairs and time periods.

**Implementation**: Our algorithm generates dynamic hedge ratios (0-1) based on market conditions rather than fixed percentages.

### 2. Carry Signal Dominance
**Research Finding**: Interest rate differentials are the primary driver of FX hedging decisions. Negative carry environments justify higher hedging.

**Implementation**: 
- Primary signal weight: 70% to carry (interest rate differential)
- Current calculation: BNM rate - Fed rate = 3.00% - 4.33% = -1.33%
- Logic: Negative differential increases hedging recommendation

### 3. Momentum Signal Value
**Research Finding**: 12-month currency momentum provides meaningful additional information for hedging decisions.

**Implementation**:
- Secondary signal weight: 30% to momentum
- Calculation: 12-month MYR/USD return performance
- Current: MYR strengthened 10.68%, reducing hedging need

### 4. Signal Combination
**Research Finding**: Multi-factor approaches combining carry, momentum, and value signals deliver superior risk-adjusted returns.

**Implementation**:
- Weighted combination: 70% carry + 30% momentum
- Future enhancement: PPP value signal integration planned

## Methodology Validation

### Academic Principles Followed
1. **Dynamic Adjustment**: Hedge ratios respond to changing market conditions
2. **Risk Management Focus**: Prioritizes protection over return optimization
3. **Signal Weighting**: Evidence-based allocation favoring carry signal
4. **Empirical Validation**: Algorithm tested against real market data

### Implementation Differences
- **Simplified Approach**: Uses weighted average vs. complex optimization
- **Business Focus**: Tailored for corporate risk management vs. portfolio optimization
- **Single Currency Pair**: MYR/USD specific vs. multi-currency analysis
- **Real-Time Application**: Live market data vs. historical backtesting focus

## Academic Support for Key Decisions

### Carry Signal Implementation
The research demonstrates that "FX returns are always negative when the interest rate differential is negative," directly supporting our algorithm's response to the current -1.33% BNM-Fed differential.

### Momentum Signal Logic
12-month currency returns provide predictive power for future FX movements, validating our momentum signal calculation showing MYR's 10.68% strengthening.

### Dynamic Hedging Benefits
The paper shows dynamic strategies delivering 100+ basis points annual outperformance over static approaches across 14 developed markets.

## Original Research Contributions

While inspired by the academic research, this implementation includes:

1. **Original Code**: All algorithm implementation is independently developed
2. **Business Application**: Specific Malaysian importer use case analysis
3. **Real-Time Integration**: Live data feeds from Yahoo Finance and FRED API
4. **Operational Framework**: Production-ready system with error handling
5. **Economic Analysis**: Detailed cost-benefit analysis for business application

## Disclaimer

This implementation represents an independent interpretation and application of academic research concepts. The algorithm code, business analysis, and technical implementation are original works. Users should refer to the original academic paper for complete research methodology and empirical results.

## References

Castro, P., Hamill, C., Harber, J., Harvey, C.R., & van Hemert, O. (2025). "The Best Strategies for FX Hedging." Available at SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5047797

Additional methodology references available in the paper's comprehensive bibliography covering 50+ years of FX hedging research.