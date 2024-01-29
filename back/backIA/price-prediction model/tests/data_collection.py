import pytest
import requests
import pandas as pd

fmp_api_key = "d3adc0ad134894b7b1bf044e468e5c69"


def test_get_nasdaq_constituent():

    nasdaq_constituent = requests.get(
        f"https://financialmodelingprep.com/api/v3/nasdaq_constituent?apikey={fmp_api_key}")
    df = pd.DataFrame(nasdaq_constituent.json())
    assert not df.empty


def test_getstockpricehistory():
    stock = "AAPL"  
    request = requests.get(
        url=f"https://financialmodelingprep.com/api/v3/historical-chart/1day/{stock}?apikey={fmp_api_key}")
    response = request.json()
    df = pd.json_normalize(response)

    df = df.drop_duplicates(subset='date')

    df['date'] = pd.to_datetime(df['date'])

    df = df.set_index('date').asfreq('D', method='bfill').reset_index()

    df['date'] = df['date'].dt.strftime('%d/%m/%Y')
    assert not df.empty
