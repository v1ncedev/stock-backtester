from backtester import run_backtest

if __name__ == "__main__":
    run_backtest("AAPL", "2020-01-01", "2023-01-01", short_ma=20, long_ma=50)
    run_backtest("TSLA", "2021-01-01", "2023-01-01", short_ma=10, long_ma=200)
