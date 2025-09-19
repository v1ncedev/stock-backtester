# stock-backtester
A Python-based stock backtesting tool using moving average crossover strategy with yfinance, pandas, and matplotlib.

This project started as a way for me to sharpen my skills in Python and finance. It’s a simple but professional stock backtesting tool that compares a ]moving average crossover strategy against a buy-and-hold benchmark using real historical data from Yahoo Finance. Backtesting is an essential step in evaluating trading strategies — it helps test ideas safely before risking real money. 

Features 
-Download historical stock data with yfinance
-Calculate Simple Moving Averages (SMA) with pandas 
-Generate buy/sell signals from SMA crossovers 
-Avoid lookahead bias by shifting signals 

Compute key performance metrics: 
 -CAGR (Compound Annual Growth Rate) 
 -Volatility (annualized) 
 -Sharpe Ratio 
 -Maximum Drawdown

Visualize: 
 -Cumulative returns (Buy & Hold vs Strategy)
 -Price chart with buy/sell markers
 -Flexible function: run backtests on any stock, any timeframe, any MA lengths

Installation 
Clone this repository and install the required packages:
```bash
git clone https://github.com/v1ncedev/stock-backtester.git
cd stock-backtester
pip install -r requirements.txt
