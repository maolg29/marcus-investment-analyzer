import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import time
import random
import warnings
warnings.filterwarnings('ignore')

class MarcusInvestmentAnalyzerPro:
    def __init__(self):
        # AÇÕES BRASILEIRAS - 20 principais
        self.brazilian_stocks = [
            'PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA',
            'BBAS3.SA', 'WEGE3.SA', 'RENT3.SA', 'LREN3.SA', 'B3SA3.SA',
            'MGLU3.SA', 'JBSS3.SA', 'SUZB3.SA', 'RAIL3.SA', 'VIVT3.SA',
            'ELET6.SA', 'CCRO3.SA', 'EMBR3.SA', 'CSAN3.SA', 'CSNA3.SA'
        ]

        # SMALL CAPS BRASILEIRAS - 10 selecionadas  
        self.brazilian_small = [
            'LWSA3.SA', 'PRIO3.SA', 'RDOR3.SA', 'HAPV3.SA', 'SOMA3.SA',
            'ALOS3.SA', 'MDIA3.SA', 'RECV3.SA', 'CXSE3.SA', 'TEND3.SA'
        ]

        # FIIs BRASILEIROS - 10 principais
        self.brazilian_fiis = [
            'HGLG11.SA', 'XPML11.SA', 'VISC11.SA', 'BCFF11.SA', 'BTLG11.SA',
            'MXRF11.SA', 'KNRI11.SA', 'IRDM11.SA', 'HGRE11.SA', 'KNCR11.SA'
        ]

        # AÇÕES AMERICANAS - 20 principais
        self.us_stocks = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'BRK-B',
            'V', 'JNJ', 'WMT', 'PG', 'UNH', 'HD', 'MA', 'DIS',
            'PYPL', 'ADBE', 'NFLX', 'CRM'
        ]

        # SMALL CAPS AMERICANAS - 10 selecionadas
        self.us_small = [
            'PLTR', 'RBLX', 'DKNG', 'COIN', 'ROKU', 'SQ', 'SHOP', 'SPOT', 'ZM', 'DOCU'
        ]

        # REITs AMERICANOS - 10 principais  
        self.us_reits = [
            'O', 'AMT', 'PLD', 'CCI', 'EQIX', 'WELL', 'DLR', 'PSA', 'EXR', 'AVB'
        ]

        # SETORES MAPEADOS
        self.sectors = {
            'Financeiro': ['ITUB4.SA', 'BBDC4.SA', 'BBAS3.SA', 'B3SA3.SA'],
            'Tecnologia': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA'],
            'Commodities': ['PETR4.SA', 'VALE3.SA', 'CSNA3.SA', 'CSAN3.SA'],
            'Consumo': ['ABEV3.SA', 'LREN3
