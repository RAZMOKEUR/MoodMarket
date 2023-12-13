from supabase import create_client, Client
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pandas as pd
from src.data_collection import getstockpricehistory,get_nasdaq_constituent

fmp_api_key = "d3adc0ad134894b7b1bf044e468e5c69"

# stock price supabase
url = "https://hmpdqidqpayqcernvdaq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhtcGRxaWRxcGF5cWNlcm52ZGFxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDE3MDA2NzAsImV4cCI6MjAxNzI3NjY3MH0.YqzToMAFc0Xg_8N-H5lGSwLijx9XG4queVFgVrOT0r0"


stockPriceSupabase: Client = create_client(url, key)

def save_nasdaq_constituent_to_database():

    # Convert nasdaq_constituent to DataFrame
    df = get_nasdaq_constituent()
    
    # Set up database connection
    password = quote_plus("sqn!B@U9kWS5Kh^f!S")
    engine = create_engine(f"postgresql://postgres:{password}@db.nzajymgnizugrvymblsm.supabase.co:5432/postgres")
    
    # Save DataFrame to database
    df.to_sql("nasdaq_constituent", engine, if_exists='replace',index=False)
    
    # Return 'updated' when finished
    return 'nasdaq_constituent updated'


def saveStockPriceHistory(stock):

    # get stock price history 
    df = getstockpricehistory(stock)

    # Set up database connection
    password = quote_plus("Gh&c&hnz3GJfNfxbRe")
    engine = create_engine(f"postgresql://postgres:{password}@db.hmpdqidqpayqcernvdaq.supabase.co:5432/postgres")

    # Save DataFrame to database
    df.to_sql(stock, engine, if_exists='replace',index=False)
    
    return f'{stock} price history updated'


# loop over each stock in nasdaq_constituent and save it to db 
def updateStockPricesHistory():
    nasdaq_constituent = get_nasdaq_constituent()
    
    for stock in nasdaq_constituent['symbol']:
        print(stock)
        saveStockPriceHistory(stock)
    
    return 'stocks prices history updated'

def fetch_stock_price_history_from_supabase(table_name, columns="*"):
    response = stockPriceSupabase.table(table_name).select(columns).execute()

    return response.data

