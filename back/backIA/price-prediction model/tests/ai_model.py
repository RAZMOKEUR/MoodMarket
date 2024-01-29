import pytest
from supabase import create_client, Client
import pandas as pd
import numpy as np
import pmdarima as pm
import pickle
from data_collection import get_nasdaq_constituent

url = "https://hmpdqidqpayqcernvdaq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhtcGRxaWRxcGF5cWNlcm52ZGFxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDE3MDA6NzAsImV4cCI6MjAxNzI3NjY3MH0.YqzToMAFc0Xg_8N-H5lGSwLijx9XG4queVFgVrOT0r0"

stockPriceSupabase: Client = create_client(url, key)

@pytest.fixture
def fetch_stock_price_history_from_supabase(table_name, columns="*"):
    table_name = table_name.upper()
    response = stockPriceSupabase.table(table_name).select(columns).execute()
    df = pd.DataFrame(response.data)
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    df.set_index('date', inplace=True)
    return df

@pytest.mark.parametrize("stock", get_nasdaq_constituent()['symbol'])
def test_update_arima_models(stock):
    stock_symbol = stock
    print(stock_symbol)
    df = fetch_stock_price_history_from_supabase(stock_symbol)

    model = pm.auto_arima(df['close'], seasonal=False, trace=True,
                          suppress_warnings=True)

    model.fit(df['close'])

    with open(f'back/backIA/price-prediction model/models/{stock_symbol}.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)

    assert model is not None

