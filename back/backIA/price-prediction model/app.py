from flask import Flask, jsonify,abort
from flask_cors import CORS
import pickle
import os
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


@app.route('/stock-price-forecasting/<stock>', methods=['GET'])
def stock_price_forecasting(stock):
    stock = stock.upper()
    model_path = f'models/{stock}.pkl'

    # Check if model exists
    if not os.path.exists(model_path):
        abort(404, description="Model not found")

    # Load the model
    with open(model_path, 'rb') as file:
        model = pickle.load(file)


    forecast = model.forecast(steps=2)

    return jsonify(forecast.tolist())

if __name__ == '__main__':
    app.run(debug=True,port=5000)