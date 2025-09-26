import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import time
import random
import warnings
from typing import List, Dict
warnings.filterwarnings('ignore')

class MarcusInvestmentAnalyzerExpanded:
    def __init__(self):
        # AÇÕES BRASILEIRAS EXPANDIDAS (20 principais + setores)
        self.brazilian_large_caps = [
            'PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA', 
            'BBAS3.SA', 'WEGE3.SA', 'RENT3.SA', 'LREN3.SA', 'B3SA3.SA',
            'MGLU3.SA', 'JBSS3.SA', 'SUZB3.SA', 'RAIL3.SA', 'VIVT3.SA',
            'ELET6.SA', 'CCRO3.SA', 'EMBR3.SA', 'CSAN3.SA', 'CSNA3.SA'
        ]

        # SMALL CAPS BRASILEIRAS SELECIONADAS
        self.brazilian_small_caps = [
            'LWSA3.SA', 'PRIO3.SA', 'RDOR3.SA', 'HAPV3.SA', 'SOMA3.SA',
            'ALOS3.SA', 'MDIA3.SA', 'RECV3.SA', 'CXSE3.SA', 'TEND3.SA'
        ]

        # FIIs BRASILEIROS PRINCIPAIS
        self.brazilian_reits = [
            'HGLG11.SA', 'XPML11.SA', 'VISC11.SA', 'BCFF11.SA', 'BTLG11.SA',
            'MXRF11.SA', 'KNRI11.SA', 'IRDM11.SA', 'HGRE11.SA', 'KNCR11.SA'
        ]

        # AÇÕES AMERICANAS EXPANDIDAS (20 principais)
        self.us_large_caps = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'BRK-B',
            'V', 'JNJ', 'WMT', 'PG', 'UNH', 'HD', 'MA', 'DIS',
            'PYPL', 'ADBE', 'NFLX', 'CRM'
        ]

        # SMALL CAPS AMERICANAS
        self.us_small_caps = [
            'PLTR', 'RBLX', 'DKNG', 'COIN', 'ROKU', 'SQ', 'SHOP', 'SPOT',
            'ZM', 'DOCU', 'CRWD', 'SNOW', 'OKTA', 'TWLO', 'PINS'
        ]

        # REITs AMERICANOS
        self.us_reits = [
            'O', 'AMT', 'PLD', 'CCI', 'EQIX', 'WELL', 'DLR', 'PSA',
            'EXR', 'AVB', 'EQR', 'MAA', 'UDR', 'ESS', 'CPT'
        ]

        # MERCADOS EUROPEUS
        self.european_stocks = [
            'ASML', 'SAP', 'INGA.AS', 'RDSA.AS', 'OR.PA', 'SAN.PA',
            'ADS.DE', 'SAP.DE', 'ALV.DE', 'DTE.DE'
      
