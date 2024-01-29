import pytest
from supabase import create_client, Client
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pandas as pd
from src.data_collection import getstockpricehistory, get_nasdaq_constituent
from src.database_operation import saveStockPriceHistory

fmp_api_key = "d3adc0ad134894b7b1bf044e468e5c69"

url = "https://hmpdqidqpayqcernvdaq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhtcGRxaWRxcGF5cWNlcm52ZGFxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDE3MDA2NzAsImV4cCI6MjAxNzI3NjY3MH0.YqzToMAFc0Xg_8N-H5lGSwLijx9XG4queVFgVrOT0r0"


stockPriceSupabase: Client = create_client(url, key)


@pytest.mark.parametrize("stock", ["AAPL", "GOOG", "MSFT"])
def test_saveStockPriceHistory(stock):

    df = getstockpricehistory(stock)

    password = quote_plus("Gh&c&hnz3GJfNfxbRe")
    engine = create_engine(
        f"postgresql://postgres:{password}@db.hmpdqidqpayqcernvdaq.supabase.co:5432/postgres")

    df.to_sql(stock, engine, if_exists='replace', index=False)

    assert df.empty == False


def test_updateStockPricesHistory():
    nasdaq_constituent = get_nasdaq_constituent()

    for stock in nasdaq_constituent['symbol']:
        print(stock)
        saveStockPriceHistory(stock)

    assert len(nasdaq_constituent['symbol']) > 0


def test_fetch_stock_price_history_from_supabase():
    table_name = "AAPL"
    response = stockPriceSupabase.table(table_name).select("*").execute()

    assert response.status_code == 200
