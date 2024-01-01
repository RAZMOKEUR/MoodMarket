from flask import Flask, jsonify
from flask_cors import CORS
import json
import src.data_collection
from src.database_operation import fetch_stock_price_history_from_supabase
import pickle
from datetime import datetime

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


@app.route('/stock-price-prediction/<stock>', methods=['GET'])
def get_stock_price_prediction(stock):
    stock_symbol = stock.upper()
    with open(f'./models/{stock_symbol}.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    n_periods = 5
    fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)

    fc.index = fc.index.astype(str)
    fc_json = fc.to_json()

    fc_dict = json.loads(fc_json)

    result = [{'close': value, 'date': datetime.strptime(
        key, "%Y-%m-%d").strftime("%d/%m/%Y")} for key, value in fc_dict.items()]

    result_json = json.dumps(result)
    return result_json


if __name__ == '__main__':
    app.run(debug=True, port=5000)
