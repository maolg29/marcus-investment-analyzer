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
        self.cache = {}
        
        # BRASIL - 45 ATIVOS EXPANDIDOS
        self.brazil_stocks = {
            'Large Caps': [
                'PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA',
                'BBAS3.SA', 'WEGE3.SA', 'RENT3.SA', 'LREN3.SA', 'MGLU3.SA',
                'JBSS3.SA', 'B3SA3.SA', 'SUZB3.SA', 'RAIL3.SA', 'VIVT3.SA',
                'ELET6.SA', 'CCRO3.SA', 'EMBR3.SA', 'CSAN3.SA', 'CSNA3.SA',
                'UGPA3.SA', 'KLBN11.SA', 'CMIG4.SA', 'TAEE11.SA', 'GGBR4.SA'
            ],
            'Small Caps': [
                'LWSA3.SA', 'PRIO3.SA', 'RDOR3.SA', 'HAPV3.SA', 'SOMA3.SA',
                'ALOS3.SA', 'CYRE3.SA', 'MTRE3.SA', 'MRFG3.SA', 'PCAR3.SA'
            ],
            'FIIs': [
                'HGLG11.SA', 'XPML11.SA', 'VISC11.SA', 'BCFF11.SA', 'BTLG11.SA',
                'MXRF11.SA', 'KNRI11.SA', 'RECT11.SA', 'URPR11.SA', 'KNCR11.SA'
            ]
        }
        
        # EUA - 45 ATIVOS EXPANDIDOS
        self.usa_stocks = {
            'Large Caps': [
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'BRK-B',
                'V', 'JNJ', 'WMT', 'PG', 'UNH', 'MA', 'HD', 'DIS', 'PYPL',
                'NFLX', 'ADBE', 'CRM', 'CMCSA', 'VZ', 'T', 'KO', 'PEP'
            ],
            'Small Caps': [
                'PLTR', 'RBLX', 'DKNG', 'COIN', 'ROKU', 'SQ', 'SHOP', 'ZM',
                'DOCU', 'PTON'
            ],
            'REITs': [
                'O', 'AMT', 'PLD', 'CCI', 'EQIX', 'PSA', 'WY', 'SPG',
                'DLR', 'WELL'
            ]
        }
        
        # SETORES EXPANDIDOS
        self.sectors = {
            'Financeiro': ['ITUB4.SA', 'BBDC4.SA', 'BBAS3.SA', 'V', 'MA', 'PYPL'],
            'Tecnologia': ['WEGE3.SA', 'B3SA3.SA', 'AAPL', 'MSFT', 'GOOGL', 'NVDA'],
            'Commodities': ['PETR4.SA', 'VALE3.SA', 'CSNA3.SA', 'GGBR4.SA'],
            'Consumo': ['ABEV3.SA', 'LREN3.SA', 'MGLU3.SA', 'WMT', 'PG', 'KO'],
            'Saúde': ['JNJ', 'UNH', 'PG'],
            'Industrial': ['EMBR3.SA', 'CCRO3.SA', 'HD'],
            'Utilities': ['ELET6.SA', 'CMIG4.SA', 'TAEE11.SA'],
            'Imobiliário': ['HGLG11.SA', 'XPML11.SA', 'O', 'AMT', 'PLD']
        }

    def get_stock_data(self, ticker):
        """Coleta dados com cache e rate limiting"""
        if ticker in self.cache:
            return self.cache[ticker]
            
        try:
            delay = random.uniform(1.0, 2.0)
            time.sleep(delay)
            
            stock = yf.Ticker(ticker)
            info = stock.info or {}
            hist = stock.history(period="1y")
            
            if len(hist) == 0:
                return None
                
            data = {
                'ticker': ticker,
                'name': info.get('shortName', ticker),
                'current_price': info.get('currentPrice', hist['Close'].iloc[-1]),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'roe': info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
                'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                'debt_to_equity': info.get('debtToEquity', 0),
                'sector': info.get('sector', 'N/A'),
                'currency': 'BRL' if '.SA' in ticker else 'USD'
            }
            
            # Cálculos técnicos
            if len(hist) >= 14:
                close_prices = hist['Close']
                data['rsi'] = self.calculate_rsi(close_prices)
                data['volatility'] = close_prices.pct_change().std() * np.sqrt(252) * 100
                data['momentum_1y'] = ((close_prices.iloc[-1] / close_prices.iloc[0]) - 1) * 100
            else:
                data['rsi'] = 50
                data['volatility'] = 25
                data['momentum_1y'] = 0
                
            self.cache[ticker] = data
            return data
            
        except Exception as e:
            st.warning(f"Erro ao coletar {ticker}: {str(e)[:50]}...")
            return None

    def calculate_rsi(self, prices, period=14):
        """Calcula RSI"""
        delta = prices.diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not rsi.empty else 50

    def buffett_analysis(self, data):
        """Análise Warren Buffett expandida"""
        if not data:
            return 0, []
        
        score = 0
        reasons = []
        
        # ROE > 15%
        if data['roe'] > 15:
            score += 25
            reasons.append(f"ROE excelente: {data['roe']:.1f}%")
        elif data['roe'] > 10:
            score += 15
            reasons.append(f"ROE bom: {data['roe']:.1f}%")
            
        # P/L < 15
        if data['pe_ratio'] and 5 < data['pe_ratio'] < 15:
            score += 20
            reasons.append(f"P/L atrativo: {data['pe_ratio']:.1f}")
        elif data['pe_ratio'] and data['pe_ratio'] < 20:
            score += 10
            
        # P/VP < 1.5
        if data['pb_ratio'] and data['pb_ratio'] < 1.5:
            score += 20
            reasons.append(f"P/VP baixo: {data['pb_ratio']:.1f}")
            
        # Baixo endividamento
        if data['debt_to_equity'] and data['debt_to_equity'] < 50:
            score += 15
            reasons.append("Baixo endividamento")
            
        # Market cap (preferência grandes empresas)
        if data['market_cap'] > 10_000_000_000:  # > 10B
            score += 10
            reasons.append("Grande porte")
            
        # Dividendos (bonus)
        if data['dividend_yield'] > 2:
            score += 10
            reasons.append(f"Paga dividendos: {data['dividend_yield']:.1f}%")
            
        return score, reasons

    def barsi_analysis(self, data):
        """Análise Luiz Barsi expandida"""
        if not data:
            return 0, []
            
        score = 0
        reasons = []
        
        # Dividend Yield > 6%
        if data['dividend_yield'] > 8:
            score += 30
            reasons.append(f"DY excepcional: {data['dividend_yield']:.1f}%")
        elif data['dividend_yield'] > 6:
            score += 20
            reasons.append(f"DY bom: {data['dividend_yield']:.1f}%")
        elif data['dividend_yield'] > 3:
            score += 10
            
        # ROE > 12%
        if data['roe'] > 15:
            score += 25
            reasons.append(f"ROE excelente: {data['roe']:.1f}%")
        elif data['roe'] > 12:
            score += 15
            
        # P/L razoável
        if data['pe_ratio'] and 8 < data['pe_ratio'] < 20:
            score += 15
            reasons.append(f"P/L razoável: {data['pe_ratio']:.1f}")
            
        # Setores BEST
        best_sectors = ['Financeiro', 'Utilities', 'Imobiliário']
        ticker_sectors = []
        for sector, tickers in self.sectors.items():
            if data['ticker'] in tickers:
                ticker_sectors.append(sector)
                
        if any(sector in best_sectors for sector in ticker_sectors):
            score += 20
            reasons.append("Setor BEST")
            
        # Baixa volatilidade
        if data['volatility'] < 30:
            score += 10
            reasons.append("Baixa volatilidade")
            
        return score, reasons

    def value_analysis(self, data):
        """Análise Benjamin Graham"""
        if not data:
            return 0, []
            
        score = 0
        reasons = []
        
        # P/L < 15
        if data['pe_ratio'] and data['pe_ratio'] < 12:
            score += 25
            reasons.append(f"P/L muito baixo: {data['pe_ratio']:.1f}")
        elif data['pe_ratio'] and data['pe_ratio'] < 15:
            score += 15
            
        # P/VP < 1.2
        if data['pb_ratio'] and data['pb_ratio'] < 1.0:
            score += 30
            reasons.append(f"P/VP excelente: {data['pb_ratio']:.1f}")
        elif data['pb_ratio'] and data['pb_ratio'] < 1.5:
            score += 20
            
        # Fórmula de Graham
        if data['pe_ratio'] and data['pb_ratio']:
            graham_number = np.sqrt(22.5 * data['pe_ratio'] * data['pb_ratio'])
            if data['current_price'] < graham_number * 0.8:
                score += 25
                reasons.append("Abaixo do valor Graham")
                
        return score, reasons

    def analyze_opportunities(self, strategy, market, category, sector, custom_ticker, max_results, min_score):
        """Análise principal expandida"""
        
        # Seleção de ativos
        stocks_to_analyze = []
        
        if custom_ticker:
            stocks_to_analyze = [custom_ticker.upper()]
        else:
            if market == "Brasil":
                market_stocks = self.brazil_stocks
            else:
                market_stocks = self.usa_stocks
                
            if category == "Todos":
                for cat_stocks in market_stocks.values():
                    stocks_to_analyze.extend(cat_stocks)
            else:
                stocks_to_analyze = market_stocks.get(category, [])
                
            # Filtro por setor
            if sector != "Todos":
                sector_stocks = self.sectors.get(sector, [])
                stocks_to_analyze = [s for s in stocks_to_analyze if s in sector_stocks]
        
        # Limitar quantidade para performance
        stocks_to_analyze = stocks_to_analyze[:max_results * 2]
        
        st.info(f"🔍 Analisando {len(stocks_to_analyze)} ativos com estratégia {strategy}...")
        
        results = []
        progress_bar = st.progress(0)
        
        for i, ticker in enumerate(stocks_to_analyze):
            progress_bar.progress((i + 1) / len(stocks_to_analyze))
            st.write(f"📊 Analisando {ticker} ({i+1}/{len(stocks_to_analyze)})")
            
            data = self.get_stock_data(ticker)
            if not data:
                continue
                
            # Aplicar estratégia
            if strategy == "Warren Buffett":
                score, reasons = self.buffett_analysis(data)
            elif strategy == "Luiz Barsi":
                score, reasons = self.barsi_analysis(data)
            else:  # Value Investing
                score, reasons = self.value_analysis(data)
                
            if score >= min_score:
                results.append({
                    'ticker': data['ticker'],
                    'nome': data['name'],
                    'score': score,
                    'preço': f"{data['currency']} {data['current_price']:.2f}",
                    'p_l': f"{data['pe_ratio']:.1f}" if data['pe_ratio'] else "N/A",
                    'p_vp': f"{data['pb_ratio']:.1f}" if data['pb_ratio'] else "N/A",
                    'roe': f"{data['roe']:.1f}%",
                    'dy': f"{data['dividend_yield']:.1f}%",
                    'setor': data['sector'],
                    'motivos': " | ".join(reasons[:3])
                })
        
        progress_bar.empty()
        
        # Ordenar por score
        results = sorted(results, key=lambda x: x['score'], reverse=True)[:max_results]
        
        return results

def main():
    st.set_page_config(
        page_title="Marcus Investment Analyzer Pro",
        page_icon="📈",
        layout="wide"
    )
    
    # Header
    st.title("📈 Marcus Investment Analyzer Pro")
    st.markdown("**Análise Profissional com Estratégias dos Maiores Investidores**")
    st.success("🚀 Versão Expandida: 90 ativos analisáveis, filtros avançados, busca personalizada!")
    
    analyzer = MarcusInvestmentAnalyzer()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configurações Avançadas")
        
        strategy = st.selectbox(
            "🎯 Estratégia de Investimento:",
            ["Warren Buffett", "Luiz Barsi", "Value Investing"]
        )
        
        market = st.selectbox(
            "🌍 Mercado:",
            ["Brasil", "Estados Unidos"]
        )
        
        category = st.selectbox(
            "📊 Categoria:",
            ["Todos", "Large Caps", "Small Caps", "FIIs" if market == "Brasil" else "REITs"]
        )
        
        sector = st.selectbox(
            "🏢 Setor:",
            ["Todos", "Financeiro", "Tecnologia", "Commodities", "Consumo", "Saúde", "Industrial", "Utilities", "Imobiliário"]
        )
        
        custom_ticker = st.text_input(
            "🔍 Busca Personalizada:",
            placeholder="Ex: AAPL, PETR4.SA"
        )
        
        max_results = st.slider("📊 Máximo de Resultados:", 5, 15, 10)
        min_score = st.slider("🎯 Score Mínimo:", 20, 80, 30)
        
        analyze_button = st.button("🚀 Executar Análise Profissional", type="primary")
    
    # Documentação das estratégias
    if strategy == "Warren Buffett":
        st.markdown("## 🎯 Estratégia Warren Buffett - Buy & Hold")
        st.info("**Filosofia:** 'Tempo no mercado supera timing do mercado'")
        st.markdown("**Critérios:** ROE > 15%, P/L < 15, P/VP < 1.5, baixo endividamento, empresas de qualidade")
        
    elif strategy == "Luiz Barsi":
        st.markdown("## 💰 Estratégia Luiz Barsi - Dividendos")
        st.info("**Filosofia:** 'Viva de dividendos, compre mensalmente empresas sólidas'")
        st.markdown("**Critérios:** DY > 6%, ROE > 12%, setores BEST, payout sustentável (20-60%)")
        
    else:
        st.markdown("## 📊 Estratégia Value Investing - Benjamin Graham")
        st.info("**Filosofia:** 'Compre empresas por menos do que valem'")
        st.markdown("**Critérios:** P/L < 15, P/VP < 1.2, margem de segurança, fórmula de Graham")
    
    # Análise
    if analyze_button:
        start_time = time.time()
        
        results = analyzer.analyze_opportunities(
            strategy, market, category, sector, custom_ticker, max_results, min_score
        )
        
        end_time = time.time()
        analysis_time = end_time - start_time
        
        if results:
            st.markdown(f"## 🎯 Oportunidades Encontradas - {strategy}")
            st.markdown(f"⏱️ **Análise concluída em {analysis_time:.1f} segundos** | 💾 **Cache:** {len(analyzer.cache)} empresas")
            
            # Métricas visuais
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🎯 Oportunidades", len(results))
            with col2:
                avg_score = sum(r['score'] for r in results) / len(results)
                st.metric("📊 Score Médio", f"{avg_score:.0f}/100")
            with col3:
                sectors = [r['setor'] for r in results if r['setor'] != 'N/A']
                top_sector = max(set(sectors), key=sectors.count) if sectors else "N/A"
                st.metric("🏢 Setor Principal", top_sector)
            with col4:
                currency = "🇧🇷 BRL" if market == "Brasil" else "🇺🇸 USD"
                st.metric("💰 Moeda", currency)
            
            # Tabela de resultados
            df = pd.DataFrame(results)
            st.dataframe(
                df,
                column_config={
                    "score": st.column_config.ProgressColumn(
                        "Score", help="Pontuação da estratégia", min_value=0, max_value=100
                    )
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Download
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Análise (CSV)",
                data=csv,
                file_name=f"marcus_analysis_{strategy.lower().replace(' ', '_')}_{market.lower()}.csv",
                mime="text/csv"
            )
            
        else:
            st.warning("⚠️ Nenhuma oportunidade encontrada com os critérios atuais. Tente ajustar os parâmetros.")
    
    # Disclaimer
    st.markdown("---")
    st.markdown("### ⚠️ Importante - Disclaimer")
    st.caption("""
    Esta análise é apenas educacional e não constitui recomendação de investimento.
    Sempre faça sua própria pesquisa antes de investir.
    Consulte um assessor qualificado para decisões de investimento.
    Investimentos envolvem risco de perda do capital investido.
    Performance passada não garante resultados futuros.
    """)
    
    st.markdown("**Marcus Investment Analyzer Pro v3.0** - Baseado nas metodologias dos maiores investidores mundiais")

if __name__ == "__main__":
    main()
