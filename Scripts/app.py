from flask import Flask, jsonify
import pandas as pd
import requests
import json

app = Flask(__name__)

@app.route('/')
def inicio():
    return 'A API dos Fiis listados está no ar!'

@app.route('/fiis')
def fiisListados():
    df = pd.read_csv('../bases_tratadas/fiis.csv', encoding='utf-8', sep=';')
    df = df.drop('Unnamed: 0', axis=1)
    df.rename(columns={"P/VP": "PVP", "N COTISTAS": "NCOTISTAS", 
                   "CAGR DIVIDENDOS 3 ANOS": "CAGRDIV", 
                   "LIQUIDEZ MEDIA DIARIA": "LIQD",
                   "ULTIMO DIVIDENDO": "ULTDIV", 'VALOR PATRIMONIAL COTA': 'VPC',' CAGR VALOR CORA 3 ANOS': 'CAGRVLR', 'PERCENTUAL EM CAIXA': 'CAIXA', ' N COTAS': 'NCOTA'}, inplace=True)

    return jsonify(df.to_json(orient='table'))

@app.route('/indices')

def indicespag():
    df2 = pd.read_csv('../bases_tratadas/indice.csv', encoding='utf-8', sep=';')
    df2 = df2.drop('Unnamed: 0', axis=1)
    df2['ifix'] = df2['ifix'].str.replace(' pts', '').str.replace('.', '').str.replace(',', '.').astype(float)
    df2['CDI'] = df2['CDI'].str.replace(',', '.').str.replace('%', '').astype(float)
    return jsonify(df2.to_json(orient='table'))

app.run(debug=True)