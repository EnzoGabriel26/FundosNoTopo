import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import requests
from plotly import graph_objects as go

st.set_page_config(
    page_title="Fiis",
    page_icon="🏢",
    layout='wide'
)

st.markdown(
    f"<h1 style='font-size: 28px;'>Informações detalhadas sobre o fundo</h1>", 
    unsafe_allow_html=True
)

st.sidebar.header('Escolha um fundo')
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
    df = pd.read_csv('../bases_tratadas/fiis.csv', sep=';')

fundos = df['TICKER']

fundo_selec = st.sidebar.selectbox('Selecione um Fundo', fundos)

token = 'p6h9dwEb8FTcUM8zmW9AEJ'
rangeCotacao = '3mo'
intervalo = '1d'

url = f"https://brapi.dev/api/quote/{fundo_selec}"
params = {
    'range': f'{rangeCotacao}',
    'interval': f'{intervalo}',
    'token': f'{token}',
}
response = requests.get(url, params=params)

# Verificando o status da requisição
if response.status_code == 200:
    data = response.json()
    
    # Acessando a lista de preços históricos
    historical_data = data['results'][0]['historicalDataPrice']
    
    # Convertendo para DataFrame
    dfValor = pd.DataFrame(historical_data)
    
    # Convertendo a coluna 'date' para um formato legível (timestamp para datetime)
    dfValor['date'] = pd.to_datetime(dfValor['date'], unit='s')
else:
    print(f"Request failed with status code {response.status_code}")

df2 = df.loc[df['TICKER'] == fundo_selec]
st.markdown(
    f"<h2 style='font-size: 32px;'>{fundo_selec}</h2></div>", 
    unsafe_allow_html=True
)

colValor, colDY, colPVP, colVar, colVarP = st.columns(5)
colValor.metric('Valor da Cota', value=f"R${df2.PRECO.mean()}")
colDY.metric('Dividend Yield', value=f"{df2.DY.mean():.2f}%")
colPVP.metric('P/VP', value=f"{df2.PVP.mean():.2f}")
colVar.metric('Variação (3 meses)', value=f"R${(df2.PRECO.mean()-dfValor['close'].iat[0]):.2f}")
colVarP.metric('Variação % (3 meses)', value=f"{(((df2.PRECO.mean()-dfValor['close'].iat[0])/dfValor['close'].iat[0])*100):.2f}%")
    
grafValor = go.Figure(data=[go.Candlestick(x=dfValor['date'],
                open=dfValor['open'],
                high=dfValor['high'],
                low=dfValor['low'],
                close=dfValor['close'])])
grafValor.update_layout(xaxis_rangeslider_visible=False)
grafValor.update_xaxes(rangebreaks=[
    dict(bounds=['sat','mon']),
])
st.plotly_chart(grafValor)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric('Último Dividendo', value=f"R${df2.ULTDIV.mean():.2f}")
col2.metric('Valor Patrimonial por Cota', value=f"R${df2.VPC.mean():.2f}")
col3.metric('Patrimônio (em milhões)', value=f"R${(df2.PATRIMONIO.mean()/1000000):.2f}")
col4.metric('Percentual em Caixa', value=f"{df2.CAIXA.mean()}%")
col5.metric('Gestão', value=f"{df2.GESTAO.max()}")

col6, col7, col8, col9, col10 = st.columns(5)
col6.metric('Liquidez Diária', value=f"R${df2.LIQD.mean():.2f}")
col7.metric('Número de Cotistas', value=f"{df2.NCOTISTAS.mean():.2f}")
col8.metric('Número de Cotas', value=f"{df2.NCOTA.mean():.2f}")
col9.metric('CAGR Dividendo', value=f"{df2.CAGRDIV.mean():.2f}")
col10.metric('CAGR Valor', value=f"{df2.CAGRVLR.mean():.2f}")



