import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import time
import random
import warnings
warnings.filterwarnings('ignore')

class MarcusAnalyzer:
    def __init__(self):
        self.br_stocks = [
            'PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA',
            'BBAS3.SA', 'WEGE3.SA', 'RENT3.SA', 'LREN3.SA', 'B3SA3.SA',
            'MGLU3.SA', 'JBSS3.SA', 'RAIL3.SA', 'VIVT3.SA', 'CCRO3.SA'
        ]

        self.us_stocks = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META',
            'V', 'JNJ', 'WMT', 'PG', 'UNH', 'HD', 'MA', 'DIS'
        ]

        self.cache = {}

    def get_data(self, ticker):
        if ticker in self.cache:
            return self.cache[ticker]

        try:
            time.sleep(random.uniform(1.5, 2.5))
            stock = yf.Ticker(ticker)
            info = stock.info

            if not info:
                return None

            data = {
                'ticker': ticker,
                'name': info.get('longName', ticker)[:25],
                'price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'pe': info.get('trailingPE', 0),
                'pb': info.get('priceToBook', 0),
                'roe': info.get('returnOnEquity', 0),
                'dy': info.get('dividendYield', 0),
                'sector': info.get('sector', 'N/A')
            }

            self.cache[ticker] = data
            return data

        except Exception as e:
            st.warning(f"Erro {ticker}: {str(e)}")
            return None

    def buffett_analysis(self, stocks):
        results = []
        progress = st.progress(0)

        for i, ticker in enumerate(stocks):
            st.write(f"Analisando {ticker}...")
            data = self.get_data(ticker)

            if data and data['price'] > 0:
                score = 0
                reasons = []

                roe = (data['roe'] or 0) * 100
                pe = data['pe'] or 999
