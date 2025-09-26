import streamlit as st
import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple
import time
import warnings
import random
warnings.filterwarnings('ignore')

class MarcusInvestmentAnalyzer:
    """
    Analisador de Investimentos Marcus - Implementa estratégias dos maiores investidores
    Baseado em: Warren Buffett, Luiz Barsi, George Soros, Ray Dalio, Peter Lynch, Benjamin Graham
    VERSÃO 2.0 - Corrigido Rate Limiting
    """

    def __init__(self):
        # Reduzido número de ações para evitar rate limiting
        self.brazilian_tickers = [
            'PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA', 'BBAS3.SA',
            'WEGE3.SA', 'RENT3.SA', 'LREN3.SA', 'B3SA3.SA', 'SUZB3.SA', 'RAIL3.SA',
            'VIVT3.SA', 'ELET6.SA', 'CCRO3.SA', 'MGLU3.SA'  # Reduzido para 16 ações
        ]
        self.us_tickers = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'BRK-B', 
            'V', 'JNJ', 'WMT', 'PG', 'UNH', 'DIS', 'HD', 'MA'  # Reduzido para 16 ações
        ]
        self.cache = {}  # Cache para evitar requisições repetidas

    def get_stock_data(self, ticker: str, retry_count: int = 3) -> Dict:
        """Coleta dados fundamentalistas de uma ação com retry logic"""

        # Verificar cache primeiro
        if ticker in self.cache:
            return self.cache[ticker]

        for attempt in range(retry_count):
            try:
                # Delay progressivo para evitar rate limiting
                delay = random.uniform(0.5, 1.5) * (attempt + 1)
                time.sleep(delay)

                st.write(f"🔄 Coletando dados de {ticker} (tentativa {attempt + 1})...")

                stock = yf.Ticker(ticker)

                # Buscar informações básicas
                try:
                    info = stock.info
         
