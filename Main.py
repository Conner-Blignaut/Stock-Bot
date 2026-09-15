import sys, os
if "venv" not in sys.executable:
    os.execv(os.path.join(os.path.dirname(__file__),
     "venv", "Scripts", "python.exe"), [sys.executable, __file__])

import yfinance as yf

def load_yf_data(input):
    ticker = yf.Ticker(input)
    data = ticker.history(period="3mo")
    print(f"\n{data}")
    return data

yf_data = load_yf_data("CEG")

yf_data.info()

import matplotlib.pyplot as plt

yf_data.hist(bins=40, figsize=(12, 8))

plt.show()

def shuffle_and_split_data(data, test_ratio, rng)
    shuffled_indicies