from flask import Flask, jsonify
from flask_cors import CORS

import src.data_collection
from src.database_operation import fetch_stock_price_history_from_supabase

app = Flask(__name__)
CORS(app) 

@app.route('/hello', methods=['GET'])
def hello():
    return 'hello world'


@app.route('/stock-price-history/<stock>', methods=['GET'])
def get_stock_price_history(stock):
    stock = stock.upper()
    data = fetch_stock_price_history_from_supabase(stock)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True,port=5000)