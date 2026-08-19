import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestão de Pátio", page_icon="🚗", layout="wide")

st.title("🚗 Sistema de Gestão e Operação de Pátio")
st.markdown("---")

@st.cache_data
def load_data():
    file_path = "pátio_antigo.xlsx"
    xls = pd.ExcelFile(file_path)
    sheets = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}
    return sheets

try:
    data = load_data()
    st.sidebar.success("Planilha carregada com sucesso!")
except Exception as e:
    st.sidebar.error(f"Erro ao carregar a planilha: {e}")
    st.stop()

# Menu Lateral
menu = st.sidebar.radio(
    "Navegação",
    ["🔎 Buscar Veículo", "📍 Localizador de Pátio", "📊 Resumo de Leilões", "👮 Agentes Cadastrados"]
)

# 1. BUSCAR VEÍCULO
if menu == "🔎 Buscar Veículo":
    st.header("🔎 Consulta de Veículos")
    
    df_veiculos = data.get("Planilha2", pd.DataFrame())
    
    if not df_veiculos.empty:
        busca = st.text_input("Digite a Placa, Chassi ou GRV:")
        
        if busca:
            resultado = df_veiculos[
                df_veiculos['placa'].astype(str).str.contains(busca, case=False, na=False) |
                df_veiculos['chassi'].astype(str).str.contains(busca, case=False, na=False) |
                df_veiculos['GRV'].astype(str).str.contains(busca, case=False, na=False)
            ]
            st.dataframe(resultado, use_container_width=True)
        else:
            st.dataframe(df_veiculos, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado na aba de veículos.")

# 2. LOCALIZADOR DE PÁTIO
elif menu == "📍 Localizador de Pátio":
    st.header("📍 Localizador de Veículos no Pátio")
    df_loc = data.get("localizador Leilões ", pd.DataFrame())
    if not df_loc.empty:
        st.dataframe(df_loc.dropna(how='all'), use_container_width=True)

# 3. RESUMO DE LEILÕES
elif menu == "📊 Resumo de Leilões":
    st.header("📊 Controle e Base dos Leilões")
    df_leilao = data.get("base dos leilões ", pd.DataFrame())
    if not df_leilao.empty:
        st.dataframe(df_leilao.dropna(how='all'), use_container_width=True)

# 4. AGENTES
elif menu == "👮 Agentes Cadastrados":
    st.header("👮 Banco de Dados de Agentes")
    df_agentes = data.get("BASE DADOS AGENTES", pd.DataFrame())
    if not df_agentes.empty:
        st.dataframe(df_agentes.dropna(how='all'), use_container_width=True)
      
