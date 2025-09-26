import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import time
import random
import warnings
warnings.filterwarnings('ignore')

class MarcusInvestmentAnalyzer:
    def __init__(self):
        self.brazilian_tickers = [
            'PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA', 
            'BBAS3.SA', 'WEGE3.SA', 'RENT3.SA', 'LREN3.SA', 'B3SA3.SA'
        ]
        self.us_tickers = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 
            'BRK-B', 'V', 'JNJ', 'WMT', 'PG'
        ]
        self.cache = {}

    def safe_get_stock_data(self, ticker):
        if ticker in self.cache:
            return self.cache[ticker]

        try:
            delay = random.uniform(1.5, 3.0)
            time.sleep(delay)

            stock = yf.Ticker(ticker)
            info = stock.info

            if not info or len(info) == 0:
                return None

            data = {
                'ticker': ticker,
                'name': info.get('longName', ticker)[:30],
                'sector': info.get('sector', 'N/A'),
                'price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'pe': info.get('trailingPE', 0),
                'pb': info.get('priceToBook', 0),
                'roe': info.get('returnOnEquity', 0),
                'dy': info.get('dividendYield', 0)
            }

            self.cache[ticker] = data
            return data

        except Exception as e:
            st.warning(f"Erro coletando {ticker}: {str(e)}")
            return None

    def analyze_buffett_strategy(self, market='BR'):
        tickers = self.brazilian_tickers if market == 'BR' else self.us_tickers
        opportunities = []

        st.info("Analisando estratégia Buy & Hold de Warren Buffett...")

        progress = st.progress(0)
        status = st.empty()

        for i, ticker in enumerate(tickers):
            status.text(f"Analisando {ticker} ({i+1}/{len(tickers)})")
