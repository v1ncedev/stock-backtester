import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def run_backtest(ticker="AAPL", start="2020-01-01", end="2023-01-01", short_ma=20, long_ma=50):
    """
    Run a simple moving average crossover backtest.

    Parameters:
        ticker (str): Stock ticker (e.g. "AAPL", "TSLA")
        start (str): Start date (YYYY-MM-DD)
        end (str): End date (YYYY-MM-DD)
        short_ma (int): Short-term moving average window
        long_ma (int): Long-term moving average window
    """

    # ------------------------------
    # 1. Download Stock Data
    # ------------------------------
    data = yf.download(ticker, start=start, end=end)

    # ------------------------------
    # 2. Create Moving Averages
    # ------------------------------
    data[f"SMA{short_ma}"] = data['Close'].rolling(window=short_ma).mean()
    data[f"SMA{long_ma}"] = data['Close'].rolling(window=long_ma).mean()

    # ------------------------------
    # 3. Generate Trading Signals
    # ------------------------------
    data['Signal'] = 0
    data.loc[data[f"SMA{short_ma}"] > data[f"SMA{long_ma}"], 'Signal'] = 1
    data.loc[data[f"SMA{short_ma}"] < data[f"SMA{long_ma}"], 'Signal'] = -1

    # Shift by 1 day to avoid lookahead bias
    data['Position'] = data['Signal'].shift(1)

    # ------------------------------
    # 4. Calculate Returns
    # ------------------------------
    data['Market Return'] = data['Close'].pct_change()
    data['Strategy Return'] = data['Market Return'] * data['Position']

    data['Cumulative Market'] = (1 + data['Market Return']).cumprod()
    data['Cumulative Strategy'] = (1 + data['Strategy Return']).cumprod()

    # ------------------------------
    # 5. Buy/Sell Points
    # ------------------------------
    buy_signals = data[(data['Position'] == 1) & (data['Position'].shift(1) != 1)]
    sell_signals = data[(data['Position'] == -1) & (data['Position'].shift(1) != -1)]

    # ------------------------------
    # 6. Performance Metrics
    # ------------------------------
    days = (data.index[-1] - data.index[0]).days

    # CAGR
    cagr_market = (data['Cumulative Market'].iloc[-1]) ** (365.0/days) - 1
    cagr_strategy = (data['Cumulative Strategy'].iloc[-1]) ** (365.0/days) - 1

    # Volatility (annualized)
    vol_market = data['Market Return'].std() * np.sqrt(252)
    vol_strategy = data['Strategy Return'].std() * np.sqrt(252)

    # Sharpe ratio
    sharpe_market = cagr_market / vol_market
    sharpe_strategy = cagr_strategy / vol_strategy

    # Max Drawdown
    def max_drawdown(series):
        cumulative = (1 + series).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        return drawdown.min()

    max_dd_market = max_drawdown(data['Market Return'])
    max_dd_strategy = max_drawdown(data['Strategy Return'])

    # Print metrics to console
    print(f"\n=== {ticker} Performance Metrics ===")
    print(f"Period: {start} → {end}")
    print(f"Short MA: {short_ma}, Long MA: {long_ma}\n")

    print(f"Buy & Hold CAGR:   {cagr_market:.2%}")
    print(f"Strategy CAGR:     {cagr_strategy:.2%}\n")

    print(f"Buy & Hold Sharpe: {sharpe_market:.2f}")
    print(f"Strategy Sharpe:   {sharpe_strategy:.2f}\n")

    print(f"Buy & Hold MaxDD:  {max_dd_market:.2%}")
    print(f"Strategy MaxDD:    {max_dd_strategy:.2%}")

    # ------------------------------
    # 7. Plot Results
    # ------------------------------
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,10), sharex=True)

    # Top plot: cumulative returns
    ax1.plot(data['Cumulative Market'], label='Buy and Hold', color='blue')
    ax1.plot(data['Cumulative Strategy'], label='Strategy', color='orange')
    ax1.set_title(f"{ticker}: Strategy vs Buy and Hold")
    ax1.legend()

    # Metrics text box OUTSIDE chart area (top-left margin)
    metrics_text = (
        f"Buy & Hold CAGR: {cagr_market:.2%}\n"
        f"Strategy CAGR: {cagr_strategy:.2%}\n\n"
        f"Buy & Hold Sharpe: {sharpe_market:.2f}\n"
        f"Strategy Sharpe: {sharpe_strategy:.2f}\n\n"
        f"Buy & Hold MaxDD: {max_dd_market:.2%}\n"
        f"Strategy MaxDD: {max_dd_strategy:.2%}"
    )

    ax1.annotate(metrics_text, xy=(0, 1), xycoords='axes fraction',
                 xytext=(-120, 0), textcoords='offset points',
                 ha='left', va='top',
                 fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

    # Bottom plot: price chart with signals
    ax2.plot(data['Close'], label=f'{ticker} Price', alpha=0.6, color='black')
    ax2.plot(data[f"SMA{short_ma}"], label=f"SMA{short_ma}", color='green', alpha=0.9)
    ax2.plot(data[f"SMA{long_ma}"], label=f"SMA{long_ma}", color='red', alpha=0.9)

    # Buy markers
    ax2.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='g', label='Buy')
    # Sell markers
    ax2.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='r', label='Sell')

    ax2.set_title("Trading Signals on Price Chart")
    ax2.legend()

    plt.tight_layout()
    plt.show()

