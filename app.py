import streamlit as st

def main():
    st.title("🎯 Marcus Investment Analyzer - TEST")
    st.success("✅ Aplicação carregou com sucesso!")
    
    st.write("Se você está vendo esta mensagem, o Streamlit está funcionando.")
    
    if st.button("Teste de Funcionamento"):
        st.balloons()
        st.write("🎉 Botão funcionando perfeitamente!")

if __name__ == "__main__":
    main()
