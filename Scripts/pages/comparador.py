import streamlit as st
import numpy as np
import pandas as pd
import requests
import sqlite3

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

try:
    cnx = sqlite3.connect('../bases_tratadas/banco_fiis.db')
except:
    cnx = sqlite3.connect('bases_tratadas/banco_fiis.db')


df = pd.read_sql('SELECT * FROM fiis', con=cnx)
df2 = pd.read_sql('SELECT * FROM indices', con=cnx)

def number_format(n):
    return f"{n:.2f}".replace(',', '*').replace('.',',').replace('*','.')

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
                        <div style='text-align: center; font-size: 20px; height: 70px;'; >{item['nome']}<br><span style='text-align: center; font-size: 28px'>{item['tipo']} {number_format(item['column'].mean())}{item['tipo2']}</span></div>""",                  
                        unsafe_allow_html=True)
                st.write("---")         
            
else:
    st.write('Selecione de 2 a 5 fundos para comparação.')