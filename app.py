import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import plotly.express as px
import time
import random
import warnings
warnings.filterwarnings('ignore')

class MarcusInvestmentAnalyzer:
    def __init__(self):
        self.brazilian_tickers = [
            'PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA', 'BBAS3.SA',
            'WEGE3.SA', 'RENT3.SA', 'LREN3.SA', 'B3SA3.SA', 'SUZB3.SA', 'RAIL3.SA'
        ]
        self.us_tickers = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'BRK-B', 
            'V', 'JNJ', 'WMT', 'PG', 'UNH', 'DIS', 'HD', 'MA'
        ]
        self.cache = {}

    def get_stock_data(self, ticker):
        if ticker in self.cache:
            return self.cache[ticker]

        try:
            delay = random.uniform(1.0, 2.0)
            time.sleep(delay)

            st.write(f"🔄 Analisando {ticker}...")

            stock = yf.Ticker(ticker)
            info = stock.info

            data = {
                'ticker': ticker,
                'name': info.get('longName', ticker),
                'sector': info.get('sector', 'N/A'),
                'current_price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'pe_ratio': info.get('trailingPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'roe': info.get('returnOnEquity', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'revenue_growth': info.get('revenueGrowth', 0)
            }

            self.cache[ticker] = data
            return data

        except Exception as e:
            st.warning(f"Erro ao coletar {ticker}: {str(e)}")
            return None

    def analyze_stocks(self, market='BR'):
        tickers = self.brazilian_tickers if market == 'BR' else self.us_tickers
        opportunities = []

        st.info("🔍 Analisando oportunidades de investimento...
