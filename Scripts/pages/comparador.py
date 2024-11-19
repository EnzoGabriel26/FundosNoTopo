import streamlit as st
import numpy as np
import pandas as pd
import requests

st.set_page_config(
    page_title="Comparador de Fiis",
    page_icon="🆚",
    layout='wide'
)

st.markdown(
    f"<h1 style='font-size: 28px;'>Comparador de Fiis</h1>", 
    unsafe_allow_html=True
)
st.sidebar.header('Escolha de dois a cinco fundos para comparar')

# URL api
url = "http://127.0.0.1:5000/fiis"

# Fazer a requisição para a API Flask
try:
    response = requests.get(url)
    if response.status_code == 200:
    # Carregar os dados do JSON no formato 'table' para um DataFrame
        json_data = response.json()
        df = pd.read_json(json_data, orient='table')
    else:
        st.error("Erro ao carregar dados da API.")
except:
    #caso o streamlit não acesse a url
    df = pd.read_csv('bases_tratadas/fiis.csv', encoding='utf-8', sep=';')
    df.rename(columns={"P/VP": "PVP", "N COTISTAS": "NCOTISTAS", 
                   "CAGR DIVIDENDOS 3 ANOS": "CAGRDIV", 
                   "LIQUIDEZ MEDIA DIARIA": "LIQD",
                   "ULTIMO DIVIDENDO": "ULTDIV", 'VALOR PATRIMONIAL COTA': 'VPC',' CAGR VALOR CORA 3 ANOS': 'CAGRVLR', 'PERCENTUAL EM CAIXA': 'CAIXA', ' N COTAS': 'NCOTA'}, inplace=True)

fundos = df['TICKER'].unique()
fundos_selec = st.sidebar.multiselect('Selecione um Fundo', fundos)
# Filtrar os fundos selecionados
df2 = df.loc[df['TICKER'].isin(fundos_selec)]


# Verificar se o número de fundos está dentro do esperado
if 2 <= len(fundos_selec) <= 5:
    cols = st.columns(len(fundos_selec))
    
    for col, fundo in zip(cols, fundos_selec):
        with col:
            st.write("---")
            st.markdown(f"<h3 style='text-align: center;'>{fundo}</h3>", unsafe_allow_html=True)
            st.write("---")
            fundo_filtrado = df2[df2['TICKER'] == fundo]

            itensComparador = [{'nome': 'Preço do Fundo:', 'column': fundo_filtrado.PRECO, 'tipo': 'R$', 'tipo2': ''}, 
                               {'nome': 'Dividend Yield:', 'column': fundo_filtrado.DY, 'tipo': '', 'tipo2': '%'},
                               {'nome': 'Último Dividendo', 'column': fundo_filtrado.ULTDIV, 'tipo': 'R$', 'tipo2': ''},
                               {'nome': 'P/VP', 'column': fundo_filtrado.PVP, 'tipo': '', 'tipo2': ''},
                               {'nome': 'Valor Patrimonial por Cota', 'column': fundo_filtrado.VPC, 'tipo': 'R$', 'tipo2': ''},
                               {'nome': 'Patrimônio', 'column': fundo_filtrado.PATRIMONIO, 'tipo': 'R$', 'tipo2': ''},
                               {'nome': 'CAGR de Dividendos', 'column': fundo_filtrado.CAGRDIV, 'tipo': '', 'tipo2': ''},
                               {'nome': 'CAGR de Valor Patrimonial', 'column': fundo_filtrado.CAGRVLR, 'tipo': '', 'tipo2': ''},
                               {'nome': 'Liquidez Diária', 'column': fundo_filtrado.LIQD, 'tipo': '', 'tipo2': ''},
                               {'nome': 'Número de Cotistas', 'column': fundo_filtrado.NCOTISTAS, 'tipo': '', 'tipo2': ''}
                               ]
            for item in itensComparador:
                st.write(f"""                  
                        <div style='text-align: center; font-size: 20px; height: 70px;'; >{item['nome']}<br><span style='text-align: center; font-size: 28px'>{item['tipo']} {item['column'].mean():.2f}{item['tipo2']}</span></div>""",                  
                        unsafe_allow_html=True)
                st.write("---")         
            
else:
    st.write('Selecione de 2 a 5 fundos para comparação.')