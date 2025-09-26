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
warnings.filterwarnings('ignore')

class MarcusInvestmentAnalyzer:
    """
    Analisador de Investimentos Marcus - Implementa estratégias dos maiores investidores
    Baseado em: Warren Buffett, Luiz Barsi, George Soros, Ray Dalio, Peter Lynch, Benjamin Graham
    """

    def __init__(self):
        self.brazilian_tickers = self.get_brazilian_top_stocks()
        self.us_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'BRK-B', 
                          'V', 'JNJ', 'WMT', 'PG', 'UNH', 'DIS', 'HD', 'MA', 'PYPL', 
                          'VZ', 'ADBE', 'NFLX', 'CRM', 'T', 'PFE', 'KO', 'PEP', 'INTC']

    def get_brazilian_top_stocks(self):
        """Retorna principais ações brasileiras baseadas no Ibovespa"""
        return ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA', 'BBAS3.SA',
                'WEGE3.SA', 'RENT3.SA', 'LREN3.SA', 'MGLU3.SA', 'JBSS3.SA', 'B3SA3.SA',
                'SUZB3.SA', 'RAIL3.SA', 'VIVT3.SA', 'ELET6.SA', 'CCRO3.SA', 'EMBR3.SA',
                'CSAN3.SA', 'CSNA3.SA', 'UGPA3.SA', 'KLBN11.SA', 'CMIG4.SA', 'TAEE11.SA']

    def get_stock_data(self, ticker: str) -> Dict:
        """Coleta dados fundamentalistas de uma ação"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="2y")

            # Dados básicos
            data = {
                'ticker': ticker,
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'current_price': info.get('currentPrice', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'roe': info.get('returnOnEquity', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'payout_ratio': info.get('payoutRatio', 0),
                'revenue_growth': info.get('revenueGrowth', 0),
                'earnings_growth': info.get('earningsGrowth', 0),
                'book_value': info.get('bookValue', 0),
                'price_to_sales': info.get('priceToSalesTrailing12Months', 0),
                'forward_pe': info.get('forwardPE', 0),
                'beta': info.get('beta', 1.0),
                'rsi': self.calculate_rsi(hist['Close']) if len(hist) > 14 else 50,
                '52w_high': info.get('fiftyTwoWeekHigh', 0),
                '52w_low': info.get('fiftyTwoWeekLow', 0)
            }

            # Calcular algumas métricas adicionais
            if len(hist) >= 252:  # 1 ano de dados
                data['volatility'] = hist['Close'].pct_change().std() * np.sqrt(252)
                data['momentum_1y'] = (hist['Close'].iloc[-1] / hist['Close'].iloc[-252] - 1) * 100

            return data
        except Exception as e:
            st.error(f"Erro ao coletar dados de {ticker}: {str(e)}")
            return None

    def calculate_rsi(self, prices, period=14):
        """Calcula RSI (Relative Strength Index)"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs)).iloc[-1]

    def buffett_buy_and_hold_strategy(self, market='BR'):
        """
        Estratégia Warren Buffett - Buy and Hold
        Critérios: ROE > 15%, P/VP < 1.5, empresas de qualidade, margem de segurança
        """
        tickers = self.brazilian_tickers if market == 'BR' else self.us_tickers
        opportunities = []

        st.info("🔍 Analisando estratégia Buy & Hold de Warren Buffett...")
        progress_bar = st.progress(0)

        for i, ticker in enumerate(tickers):
            data = self.get_stock_data(ticker)
            if data:
                # Critérios Buffett
                roe = data.get('roe', 0) * 100 if data.get('roe') else 0
                pb_ratio = data.get('pb_ratio', 999)
                pe_ratio = data.get('pe_ratio', 999)
                debt_equity = data.get('debt_to_equity', 999)
                revenue_growth = data.get('revenue_growth', 0) * 100 if data.get('revenue_growth') else 0

                # Score Buffett (0-100)
                score = 0
                reasons = []

                if roe > 15:
                    score += 25
                    reasons.append(f"ROE excelente: {roe:.1f}%")
                elif roe > 10:
                    score += 15
                    reasons.append(f"ROE bom: {roe:.1f}%")

                if 0 < pb_ratio < 1.5:
                    score += 20
                    reasons.append(f"P/VP atrativo: {pb_ratio:.2f}")
                elif 0 < pb_ratio < 2.0:
                    score += 10
                    reasons.append(f"P/VP razoável: {pb_ratio:.2f}")

                if 0 < pe_ratio < 15:
                    score += 20
                    reasons.append(f"P/L baixo: {pe_ratio:.1f}")
                elif 0 < pe_ratio < 25:
                    score += 10
                    reasons.append(f"P/L moderado: {pe_ratio:.1f}")

                if debt_equity < 50:
                    score += 15
                    reasons.append("Baixo endividamento")

                if revenue_growth > 5:
                    score += 10
                    reasons.append(f"Crescimento receita: {revenue_growth:.1f}%")

                if data.get('sector') in ['Consumer Defensive', 'Healthcare', 'Utilities', 'Consumer Cyclical']:
                    score += 10
                    reasons.append("Setor defensivo")

                if score >= 50:  # Threshold para Buffett
                    opportunities.append({
                        'Ticker': ticker,
                        'Nome': data.get('name', 'N/A')[:30],
                        'Setor': data.get('sector', 'N/A'),
                        'Preço': f"${data.get('current_price', 0):.2f}",
                        'P/L': f"{pe_ratio:.1f}" if pe_ratio < 999 else "N/A",
                        'P/VP': f"{pb_ratio:.2f}" if pb_ratio < 999 else "N/A", 
                        'ROE': f"{roe:.1f}%",
                        'Score': f"{score}/100",
                        'Motivos': " | ".join(reasons[:3])
                    })

            progress_bar.progress((i + 1) / len(tickers))
            time.sleep(0.1)  # Rate limiting

        return sorted(opportunities, key=lambda x: int(x['Score'].split('/')[0]), reverse=True)

    def barsi_dividends_strategy(self, market='BR'):
        """
        Estratégia Luiz Barsi - Foco em Dividendos
        Critérios: DY > 6%, Payout < 60%, setores BEST, consistência
        """
        tickers = self.brazilian_tickers if market == 'BR' else self.us_tickers
        opportunities = []

        st.info("💰 Analisando estratégia de Dividendos de Luiz Barsi...")
        progress_bar = st.progress(0)

        for i, ticker in enumerate(tickers):
            data = self.get_stock_data(ticker)
            if data:
                div_yield = data.get('dividend_yield', 0) * 100 if data.get('dividend_yield') else 0
                payout = data.get('payout_ratio', 0) * 100 if data.get('payout_ratio') else 0
                roe = data.get('roe', 0) * 100 if data.get('roe') else 0

                # Score Barsi (0-100)
                score = 0
                reasons = []

                if div_yield > 6:
                    score += 30
                    reasons.append(f"DY alto: {div_yield:.1f}%")
                elif div_yield > 4:
                    score += 20
                    reasons.append(f"DY bom: {div_yield:.1f}%")

                if 0 < payout < 60:
                    score += 25
                    reasons.append(f"Payout sustentável: {payout:.1f}%")
                elif 0 < payout < 80:
                    score += 15
                    reasons.append(f"Payout moderado: {payout:.1f}%")

                if roe > 12:
                    score += 20
                    reasons.append(f"ROE sólido: {roe:.1f}%")

                # Setores BEST (Bancos, Energia, Saneamento, Telecomunicações)
                best_sectors = ['Financial Services', 'Utilities', 'Energy', 'Communication Services']
                if data.get('sector') in best_sectors:
                    score += 15
                    reasons.append("Setor BEST")

                # Estabilidade (baixa volatilidade)
                if data.get('beta', 1) < 1.2:
                    score += 10
                    reasons.append("Baixa volatilidade")

                if score >= 45:  # Threshold para Barsi
                    opportunities.append({
                        'Ticker': ticker,
                        'Nome': data.get('name', 'N/A')[:30],
                        'Setor': data.get('sector', 'N/A'),
                        'Preço': f"${data.get('current_price', 0):.2f}",
                        'DY': f"{div_yield:.1f}%",
                        'Payout': f"{payout:.1f}%" if payout > 0 else "N/A",
                        'ROE': f"{roe:.1f}%",
                        'Score': f"{score}/100",
                        'Motivos': " | ".join(reasons[:3])
                    })

            progress_bar.progress((i + 1) / len(tickers))
            time.sleep(0.1)

        return sorted(opportunities, key=lambda x: int(x['Score'].split('/')[0]), reverse=True)

    def swing_trade_strategy(self, market='BR'):
        """
        Estratégia Swing Trade
        Critérios: RSI, momentum, breakouts, análise técnica
        """
        tickers = self.brazilian_tickers if market == 'BR' else self.us_tickers
        opportunities = []

        st.info("📈 Analisando oportunidades de Swing Trade...")
        progress_bar = st.progress(0)

        for i, ticker in enumerate(tickers):
            data = self.get_stock_data(ticker)
            if data:
                rsi = data.get('rsi', 50)
                current_price = data.get('current_price', 0)
                high_52w = data.get('52w_high', 0)
                low_52w = data.get('52w_low', 0)

                # Score Swing Trade (0-100)
                score = 0
                reasons = []
                signals = []

                # RSI Analysis
                if 30 <= rsi <= 40:
                    score += 25
                    reasons.append("RSI oversold")
                    signals.append("🟢 COMPRA")
                elif 60 <= rsi <= 70:
                    score += 15
                    reasons.append("RSI forte")
                    signals.append("🟡 ATENÇÃO")
                elif rsi > 70:
                    signals.append("🔴 VENDA")
                    reasons.append("RSI overbought")

                # Posição no range 52w
                if high_52w > 0 and low_52w > 0:
                    position_in_range = (current_price - low_52w) / (high_52w - low_52w)

                    if position_in_range < 0.3:
                        score += 20
                        reasons.append("Próximo mínima 52w")
                        if "🟢 COMPRA" not in signals:
                            signals.append("🟢 COMPRA")
                    elif position_in_range > 0.8:
                        score += 10
                        reasons.append("Próximo máxima 52w")
                        signals.append("🔴 VENDA")

                # Volume e momentum
                momentum_1y = data.get('momentum_1y', 0)
                if momentum_1y > 20:
                    score += 15
                    reasons.append(f"Momentum forte: {momentum_1y:.1f}%")

                # Volatilidade (oportunidade para swing)
                volatility = data.get('volatility', 0)
                if 0.2 < volatility < 0.6:
                    score += 10
                    reasons.append("Volatilidade ideal")

                if score >= 35 or any("🟢" in s or "🔴" in s for s in signals):
                    opportunities.append({
                        'Ticker': ticker,
                        'Nome': data.get('name', 'N/A')[:30],
                        'Preço': f"${current_price:.2f}",
                        'RSI': f"{rsi:.1f}",
                        'Sinal': " ".join(signals) or "🟡 NEUTRO",
                        'Momentum 1Y': f"{momentum_1y:.1f}%" if momentum_1y else "N/A",
                        'Score': f"{score}/100",
                        'Motivos': " | ".join(reasons[:3])
                    })

            progress_bar.progress((i + 1) / len(tickers))
            time.sleep(0.1)

        return sorted(opportunities, key=lambda x: int(x['Score'].split('/')[0]), reverse=True)

    def value_investing_graham_strategy(self, market='BR'):
        """
        Estratégia Benjamin Graham - Value Investing Clássico
        Critérios: P/L < 15, P/VP < 1.5, margem de segurança
        """
        tickers = self.brazilian_tickers if market == 'BR' else self.us_tickers
        opportunities = []

        st.info("💎 Analisando oportunidades Value Investing (Graham)...")
        progress_bar = st.progress(0)

        for i, ticker in enumerate(tickers):
            data = self.get_stock_data(ticker)
            if data:
                pe_ratio = data.get('pe_ratio', 999)
                pb_ratio = data.get('pb_ratio', 999)
                current_price = data.get('current_price', 0)
                book_value = data.get('book_value', 0)

                # Score Graham (0-100)
                score = 0
                reasons = []

                # P/L baixo
                if 0 < pe_ratio < 10:
                    score += 30
                    reasons.append(f"P/L muito baixo: {pe_ratio:.1f}")
                elif 0 < pe_ratio < 15:
                    score += 20
                    reasons.append(f"P/L baixo: {pe_ratio:.1f}")

                # P/VP baixo
                if 0 < pb_ratio < 1:
                    score += 25
                    reasons.append(f"P/VP < 1: {pb_ratio:.2f}")
                elif 0 < pb_ratio < 1.5:
                    score += 15
                    reasons.append(f"P/VP baixo: {pb_ratio:.2f}")

                # Fórmula de Graham: √(22.5 × EPS × Book Value per Share)
                if pe_ratio > 0 and pb_ratio > 0 and pe_ratio < 999 and pb_ratio < 999:
                    graham_number = np.sqrt(22.5 / (pe_ratio * pb_ratio))
                    if graham_number > 1:
                        score += 20
                        reasons.append("Fórmula Graham positiva")

                # Consistência financeira
                debt_equity = data.get('debt_to_equity', 999)
                if debt_equity < 50:
                    score += 15
                    reasons.append("Baixo endividamento")

                # Margem de segurança baseada no P/VP
                if 0 < pb_ratio < 0.8:
                    score += 10
                    reasons.append("Grande margem segurança")

                if score >= 40:  # Threshold para Graham
                    opportunities.append({
                        'Ticker': ticker,
                        'Nome': data.get('name', 'N/A')[:30],
                        'Setor': data.get('sector', 'N/A'),
                        'Preço': f"${current_price:.2f}",
                        'P/L': f"{pe_ratio:.1f}" if pe_ratio < 999 else "N/A",
                        'P/VP': f"{pb_ratio:.2f}" if pb_ratio < 999 else "N/A",
                        'Score': f"{score}/100",
                        'Motivos': " | ".join(reasons[:3])
                    })

            progress_bar.progress((i + 1) / len(tickers))
            time.sleep(0.1)

        return sorted(opportunities, key=lambda x: int(x['Score'].split('/')[0]), reverse=True)

def main():
    st.set_page_config(
        page_title="Marcus Investment Analyzer",
        page_icon="📈",
        layout="wide"
    )

    # Header
    st.title("📈 Marcus Investment Analyzer")
    st.markdown("### Analisador baseado nas estratégias dos maiores investidores mundiais")
    st.markdown("**Warren Buffett • Luiz Barsi • George Soros • Ray Dalio • Peter Lynch • Benjamin Graham**")

    # Sidebar
    st.sidebar.markdown("## ⚙️ Configurações")

    # Seleção da estratégia
    strategy = st.sidebar.selectbox(
        "Escolha a Estratégia:",
        [
            "🎯 Buy & Hold (Warren Buffett)",
            "💰 Dividendos (Luiz Barsi)", 
            "📈 Swing Trade",
            "💎 Value Investing (Benjamin Graham)",
        ]
    )

    # Seleção do mercado
    market = st.sidebar.selectbox(
        "Mercado:",
        ["🇧🇷 Brasil (B3)", "🇺🇸 Estados Unidos (NYSE/NASDAQ)"]
    )
    market_code = "BR" if "Brasil" in market else "US"

    # Número de resultados
    num_results = st.sidebar.slider("Número de oportunidades:", 5, 20, 10)

    # Botão de análise
    analyze_button = st.sidebar.button("🚀 Analisar Oportunidades", type="primary")

    # Informações da estratégia selecionada
    if "Buy & Hold" in strategy:
        st.markdown("""
        ## 🎯 Estratégia Buy & Hold - Warren Buffett
        **Filosofia:** "Tempo no mercado supera timing do mercado"

        **Critérios:**
        - ROE > 15% (empresas rentáveis)
        - P/VP < 1.5 (preço justo) 
        - P/L < 25 (não pagar caro)
        - Baixo endividamento
        - Empresas de qualidade em setores defensivos
        """)

    elif "Dividendos" in strategy:
        st.markdown("""
        ## 💰 Estratégia Dividendos - Luiz Barsi  
        **Filosofia:** "Viver de renda com disciplina e paciência"

        **Critérios:**
        - Dividend Yield > 6%
        - Payout Ratio < 60% (sustentabilidade)
        - Setores BEST (Bancos, Energia, Saneamento, Telecom)
        - ROE > 12%
        - Histórico consistente de pagamentos
        """)

    elif "Swing Trade" in strategy:
        st.markdown("""
        ## 📈 Estratégia Swing Trade
        **Filosofia:** "Capturar movimentos de médio prazo (dias/semanas)"

        **Critérios:**
        - RSI entre 30-40 (oversold) ou 60-70 (momentum)
        - Posição próxima às mínimas/máximas de 52 semanas
        - Volatilidade ideal (20%-60%)
        - Análise de momentum e volume
        """)

    elif "Value Investing" in strategy:
        st.markdown("""
        ## 💎 Value Investing - Benjamin Graham
        **Filosofia:** "Comprar por menos do que vale intrinsecamente"

        **Critérios:**
        - P/L < 15 (empresas baratas)
        - P/VP < 1.5 (patrimônio líquido)
        - Fórmula de Graham válida
        - Margem de segurança > 25%
        - Baixo endividamento
        """)

    # Análise
    if analyze_button:
        analyzer = MarcusInvestmentAnalyzer()

        with st.spinner("🔄 Marcus analisando o mercado..."):
            if "Buy & Hold" in strategy:
                opportunities = analyzer.buffett_buy_and_hold_strategy(market_code)
            elif "Dividendos" in strategy:
                opportunities = analyzer.barsi_dividends_strategy(market_code)
            elif "Swing Trade" in strategy:
                opportunities = analyzer.swing_trade_strategy(market_code)
            elif "Value Investing" in strategy:
                opportunities = analyzer.value_investing_graham_strategy(market_code)

        # Resultados
        st.markdown("---")
        st.markdown(f"## 🎯 Top {num_results} Oportunidades - {strategy}")

        if opportunities:
            # Mostrar apenas o número solicitado
            opportunities = opportunities[:num_results]

            # Criar DataFrame
            df = pd.DataFrame(opportunities)

            # Mostrar tabela
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # Estatísticas
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("🎯 Oportunidades Encontradas", len(opportunities))

            with col2:
                if 'Score' in df.columns:
                    avg_score = np.mean([int(score.split('/')[0]) for score in df['Score']])
                    st.metric("📊 Score Médio", f"{avg_score:.1f}/100")

            with col3:
                if 'Setor' in df.columns:
                    most_common_sector = df['Setor'].mode().iloc[0] if not df['Setor'].mode().empty else "N/A"
                    st.metric("🏢 Setor Predominante", most_common_sector)

            # Gráfico de distribuição por setor (se aplicável)
            if 'Setor' in df.columns and len(df) > 3:
                st.markdown("### 📊 Distribuição por Setor")
                sector_counts = df['Setor'].value_counts()
                fig = px.pie(values=sector_counts.values, names=sector_counts.index, 
                           title="Oportunidades por Setor")
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("⚠️ Nenhuma oportunidade encontrada com os critérios atuais. Tente ajustar os parâmetros.")

        # Disclaimer
        st.markdown("---")
        st.markdown("""
        ### ⚠️ **Importante - Disclaimer**

        - Esta análise é **apenas educacional** e não constitui recomendação de investimento
        - **Sempre faça sua própria pesquisa** antes de investir
        - Consulte um **assessor qualificado** para decisões de investimento
        - Investimentos envolvem **risco de perda** do capital investido
        - **Performance passada não garante resultados futuros**

        **Marcus Investment Analyzer v1.0** - Baseado nas metodologias dos maiores investidores mundiais
        """)

if __name__ == "__main__":
    main()
