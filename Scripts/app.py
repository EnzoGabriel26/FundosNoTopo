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
    return jsonify(df.to_json(orient='table'))

@app.route('/indices')

def indicespag():
    df2 = pd.read_csv('../bases_tratadas/indice.csv', encoding='utf-8', sep=';')
    return jsonify(df2.to_json(orient='table'))

app.run(debug=True)