import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from plotly import graph_objects as go
import requests

# Configurações da página no Streamlit
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout='wide'
)
qtd_fundos = st.sidebar.selectbox('Selecione a quantidade de Fundos Imobiliários que deseja ver no Ranking', [100,50,30,20,10])
st.markdown(
    f"<h1 style='font-size: 28px;'>Informações sobre os {qtd_fundos} Fundos de Investimento Imobiliário com mais cotistas listados na B3</h1>", 
    unsafe_allow_html=True
)
# URL api
url = "http://127.0.0.1:5000/fiis"
url2 = "http://127.0.0.1:5000/indices"

# Fazer a requisição para a API Flask
try:
    response = requests.get(url)
    response2 = requests.get(url2)
    if response.status_code == 200:
    # Carregar os dados do JSON no formato 'table' para um DataFrame
        json_data = response.json()
        json_data2 = response2.json()
        df = pd.read_json(json_data, orient='table')
        df2 = pd.read_json(json_data2, orient='table')
    else:
        st.error("Erro ao carregar dados da API.")
except:
    #caso o streamlit não acesse a url
    df = pd.read_csv('../bases_tratadas/fiis.csv', encoding='utf-8', sep=';')
    df2 = pd.read_csv('../bases_tratadas/indice.csv', encoding='utf-8', sep=';')
    df = df.drop('Unnamed: 0', axis=1)
    df.rename(columns={"P/VP": "PVP", "N COTISTAS": "NCOTISTAS", 
                   "CAGR DIVIDENDOS 3 ANOS": "CAGRDIV", 
                   "LIQUIDEZ MEDIA DIARIA": "LIQD",
                   "ULTIMO DIVIDENDO": "ULTDIV", 'VALOR PATRIMONIAL COTA': 'VPC',' CAGR VALOR CORA 3 ANOS': 'CAGRVLR', 'PERCENTUAL EM CAIXA': 'CAIXA', ' N COTAS': 'NCOTA'}, inplace=True)
    df2 = df2.drop('Unnamed: 0', axis=1)
    df2['ifix'] = df2['ifix'].str.replace(' pts', '').str.replace('.', '').str.replace(',', '.').astype(float)
    df2['CDI'] = df2['CDI'].str.replace(',', '.').str.replace('%', '').astype(float)



dfTabela = df.copy()

df_top100 = df.nlargest(qtd_fundos, 'NCOTISTAS')

#contas para análise de gráficos
cdi = df2['CDI'].mean()
mediaDY = df_top100['DY'].mean()
medianaDY = df_top100['DY'].median()
mediaPVP = df_top100['PVP'].mean()
medianaPVP = df_top100['PVP'].median()
# Contagem de fundos acima da média de Dividend Yield
fundos_acima_media_dy = df_top100[df_top100['DY'] > mediaDY].shape[0]
# Contagem de fundos com DY maior que o CDI
fundos_acima_cdi = df_top100[df_top100['DY'] > cdi].shape[0]
# Contagem de fundos cima da mediana DY
fundos_acima_mediana_dy = df_top100[df_top100['DY'] > medianaDY].shape[0]
# Contagem de fundos com PVP maior que a média
fundos_acima_media_pvp = df_top100[df_top100['PVP'] > mediaPVP].shape[0]
# Contagem de fundos com PVP maior que 1
fundos_acima_pvp_1 = df_top100[df_top100['PVP'] > 1].shape[0]
# Contagem de fundos cima da mediana pvp
fundos_acima_mediana_pvp = df_top100[df_top100['PVP'] > medianaPVP].shape[0]


# Exibição das informações gerais sobre os Fiis
with st.expander('Informações gerais sobre os Fiis'):
    colIfix, colCdi, colNull = st.columns(3)
    colIfix.metric('IFIX', value=f"{df2.ifix.mean():.2f}")
    colCdi.metric('CDI', value=f'{df2.CDI.mean():.2f}%')

    colDY, colPVP, colCagr = st.columns(3)
    colDY.metric('Dividend Yield', value=f"{df_top100.DY.mean():.2f}%")
    colPVP.metric('P/VP', value=f"{df_top100.PVP.mean():.2f}")
    colCagr.metric('Cagr de Dividendos (últimos 3 anos)', value=f"{df_top100.CAGRDIV.mean():.2f}%")

    colLiq, colCotistas, colGestao = st.columns(3)
    colLiq.metric('Liquidez Diária Média (Milhar)', value=f"R${(df_top100.LIQD.mean()/1000):.2f}")
    colGestao.metric('Patrimônio Médio (Milhar)', value=f"R${(df_top100.PATRIMONIO.mean()/1000):.2f}")
    colCotistas.metric('Número médio de cotistas', value=f"{df_top100.NCOTISTAS.mean():.0f}")

# Exibição dos gráficos
with st.expander('Gráficos gerais sobre os Fiis'):
    colgraf1, colgraf2 = st.columns(2)
    with colgraf1:
        # Gráfico de Barras com DY
        graf1 = go.Figure(
            data=[
                go.Bar(name='Fundos DY', x=df_top100['TICKER'], y=df_top100['DY'], marker_color='#e377c2'),
                go.Scatter(name='Média', x=df_top100['TICKER'], y=[mediaDY]*len(df_top100), mode='lines'),
                go.Scatter(name='Mediana', x=df_top100['TICKER'], y=[medianaDY]*len(df_top100), mode='lines'),
            ]
        )
        graf1.update_layout(
            title='Mapeamento de Dividend Yield',
            xaxis_title='Fundo',
            yaxis_title='DY',
        )
        st.plotly_chart(graf1)
    st.markdown(f'<h4 style=font-size: 16px;>  Análise rápida </h4>', unsafe_allow_html=True)
    st.markdown(f'Nos {qtd_fundos} fundos com mais cotistas, existem {fundos_acima_media_dy} fundos que pagam acima da média do mercado ({mediaDY:.2f}%), {fundos_acima_mediana_dy} estão acima da mediana ({medianaDY:.2f}) e {fundos_acima_cdi} que pagam mais que o CDI ({cdi:.2f}%).')
    if fundos_acima_cdi > (qtd_fundos/2):
        st.markdown(f'A maioria dos fundos ({((fundos_acima_cdi/qtd_fundos)*100):.2f}%) estão pagando mais que a renda fixa.')
    else:
        st.markdown(f'A renda fixa está pagando mais que a maioria dos fundos ({((fundos_acima_cdi/qtd_fundos)*100):.2f}%)')
    with colgraf2:
        # Histograma de Dividend Yield
        graf2 = px.histogram(df_top100, x='DY', title='Histograma de Dividend Yield')
        st.plotly_chart(graf2)

    colgraf3, colgraf4 = st.columns(2)
    with colgraf3:
        # Gráfico de Barras com PVP
        graf3 = go.Figure(
            data=[
                go.Bar(name='Fundos P/VP', x=df_top100['TICKER'], y=df_top100['PVP'], marker_color='lightslategray'),
                go.Scatter(name='Média', x=df_top100['TICKER'], y=[mediaPVP]*len(df_top100), mode='lines'),
                go.Scatter(name='Mediana', x=df_top100['TICKER'], y=[medianaPVP]*len(df_top100), mode='lines'),
                go.Scatter(name='P/VP 1.0', x=df_top100['TICKER'], y=[1]*len(df_top100), mode='lines')
            ]
        )
        graf3.update_layout(
            title='Mapeamento de P/VP',
            xaxis_title='Fundo',
            yaxis_title='P/VP',
        )
        st.plotly_chart(graf3)
    st.markdown(f'<h4 style=font-size: 16px;>  Análise rápida </h4>', unsafe_allow_html=True)
    st.markdown(f'Nos {qtd_fundos} fundos com mais cotistas, existem {fundos_acima_media_pvp} fundos com o P/VP acima da média do mercado ({mediaPVP:.2f}), {fundos_acima_mediana_pvp} estão acima da mediana ({medianaPVP:.2f}) e {fundos_acima_pvp_1} que estão com o P/VP acima de 1.0')
    if fundos_acima_pvp_1 > (qtd_fundos/2):
        st.markdown(f'O valor da maioria dos fundos ({((fundos_acima_pvp_1/qtd_fundos)*100):.2f}%) estão negociando ACIMA do seu valor patrimonial. O mercado pode estar um pouco caro.')
    else:
        st.markdown(f'O valor da maioria dos fundos ({(100-((fundos_acima_pvp_1/qtd_fundos)*100)):.2f}%) estão negociando ABAIXO do seu valor patrimonial. O mercado pode estar barato.')    
    with colgraf4:
        # Histograma de Preço / Valor Patrimonial
        graf4 = px.histogram(df_top100, x='PVP', title='Histograma de Preço / Valor Patrimonial')
        st.plotly_chart(graf4)
    
    colgraf5, colgraf6 = st.columns(2)
    with colgraf5:
        # Gráfico de Dispersão
        graf5 = px.scatter(
            df_top100,
            x='NCOTISTAS',
            y='DY',
            hover_data=['TICKER'],
            color='TICKER',
            labels={'NCOTISTAS': 'Número de Cotistas', 'DY': 'Dividend Yield (%)'},
            title='Relação entre Número de Cotistas e Dividend Yield',
        )
        st.plotly_chart(graf5)
        correlacaoGraf5 = df["NCOTISTAS"].corr(df["DY"])
        st.markdown(f'<h4 style=font-size: 16px;>  Análise rápida </h4>', unsafe_allow_html=True)
        st.markdown(f'O índice de correlação entre o Número de Cotistas e o Dividend Yield é de: {correlacaoGraf5:.3f}')
        if (correlacaoGraf5 >= 0.8 or correlacaoGraf5 <= -0.8):
            st.markdown(f'Os dois tem uma correlação muito forte.')
        elif (correlacaoGraf5 >= 0.6 or correlacaoGraf5 <= -0.6):
            st.markdown(f'Os dois tem uma correlação forte.')
        elif (correlacaoGraf5 >= 0.4 or correlacaoGraf5 <= -0.4):
            st.markdown(f'Os dois tem uma correlação moderada.')
        elif (correlacaoGraf5 >= 0.2 or correlacaoGraf5 <= -0.2):
            st.markdown(f'Os dois tem uma correlação fraca.')
        else:
            st.markdown(f'Os dois tem uma correlação muito fraca ou não tem nenhuma correlação.')

    with colgraf6:
        # Gráfico de Dispersão
        graf6 = px.scatter(
            df_top100,
            x='CAGRDIV',
            y='CAGRVLR',
            hover_data=['TICKER'],
            color='TICKER',
            labels={'CAGRDIV': 'CAGR de Dividendos', 'CAGRVLR': 'CAGR de Valor'},
            title='Relação entre CAGR de Dividendos e CAGR de Valor Patrimonial',
        )
        st.plotly_chart(graf6)
        correlacaoGraf6 = df["CAGRDIV"].corr(df["CAGRVLR"])
        st.markdown(f'<h4 style=font-size: 16px;>  Análise rápida </h4>', unsafe_allow_html=True)
        st.markdown(f'O índice de correlação entre o Número de Cotistas e o Dividend Yield é de: {correlacaoGraf6:.3f}')
        if (correlacaoGraf6 >= 0.8 or correlacaoGraf6 <= -0.8):
            st.markdown(f'Os dois tem uma correlação muito forte.')
        elif (correlacaoGraf6 >= 0.6 or correlacaoGraf6 <= -0.6):
            st.markdown(f'Os dois tem uma correlação forte.')
        elif (correlacaoGraf6 >= 0.4 or correlacaoGraf6 <= -0.4):
            st.markdown(f'Os dois tem uma correlação moderada.')
        elif (correlacaoGraf6 >= 0.2 or correlacaoGraf6 <= -0.2):
            st.markdown(f'Os dois tem uma correlação fraca.')
        else:
            st.markdown(f'Os dois tem uma correlação muito fraca ou não tem nenhuma correlação.')        

    colgraf7, colgraf8 = st.columns(2)

    with colgraf7:
        # Gráfico de Pizza
        gestao_counts = df['GESTAO'].value_counts().reset_index()
        gestao_counts.columns = ['GESTAO', 'count']
        graf7 = px.pie(
            gestao_counts,
            names='GESTAO',
            values='count',
            title='Distribuição de Gestão (Ativa vs Passiva)'
        )
        st.plotly_chart(graf7)
    with colgraf8:
        # Histograma de valor
        graf8 = px.histogram(df_top100, x='PRECO', title='Histograma de Valor')
        st.plotly_chart(graf8)

# Exibição da tabela de Fiis
with st.expander('Todos os Fiis Listados'):
    st.dataframe(data=dfTabela, hide_index=True)
