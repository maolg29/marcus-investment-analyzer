import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import time
import random
import warnings
warnings.filterwarnings("ignore")

class MarcusInvestmentAnalyzer:
    def __init__(self):
        # AÇÕES BRASILEIRAS - 20 principais
        self.br_large = [
            "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "ABEV3.SA",
            "BBAS3.SA", "WEGE3.SA", "RENT3.SA", "LREN3.SA", "B3SA3.SA",
            "MGLU3.SA", "JBSS3.SA", "SUZB3.SA", "RAIL3.SA", "VIVT3.SA",
            "ELET6.SA", "CCRO3.SA", "EMBR3.SA", "CSAN3.SA", "CSNA3.SA"
        ]

        # SMALL CAPS BRASILEIRAS
        self.br_small = [
            "LWSA3.SA", "PRIO3.SA", "RDOR3.SA", "HAPV3.SA", "SOMA3.SA"
        ]

        # FIIs BRASILEIROS
        self.br_fiis = [
            "HGLG11.SA", "XPML11.SA", "VISC11.SA", "BCFF11.SA", "BTLG11.SA"
        ]

        # AÇÕES AMERICANAS - 20 principais
        self.us_large = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "BRK-B",
            "V", "JNJ", "WMT", "PG", "UNH", "HD", "MA", "DIS",
            "PYPL", "ADBE", "NFLX", "CRM"
        ]

        # SMALL CAPS AMERICANAS
        self.us_small = [
            "PLTR", "RBLX", "DKNG", "COIN", "ROKU"
        ]

        # REITs AMERICANOS
        self.us_reits = [
            "O", "AMT", "PLD", "CCI", "EQIX"
        ]

        # SETORES
        self.sectors = {
            "Financeiro": ["ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "V", "MA"],
            "Tecnologia": ["AAPL", "MSFT", "GOOGL", "NVDA", "META"],
            "Commodities": ["PETR4.SA", "VALE3.SA", "CSNA3.SA"],
            "Consumo": ["ABEV3.SA", "LREN3.SA", "WMT", "PG"],
            "Saude": ["JNJ", "UNH", "RDOR3.SA"],
            "Industrial": ["WEGE3.SA", "EMBR3.SA", "HD"]
        }

        self.cache = {}

    def get_tickers(self, category, market):
        if market == "BR":
            if category == "Large Caps":
                return self.br_large
            elif category == "Small C
