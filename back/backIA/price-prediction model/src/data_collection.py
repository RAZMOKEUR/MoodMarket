import requests
import pandas as pd 

fmp_api_key = "d3adc0ad134894b7b1bf044e468e5c69"


def get_nasdaq_constituent():
    # Make a GET request to fetch nasdaq constituent data
    nasdaq_constituent = requests.get(f"https://financialmodelingprep.com/api/v3/nasdaq_constituent?apikey={fmp_api_key}")
    df = pd.DataFrame(nasdaq_constituent.json())

    return df 

def getstockpricehistory(stock):
    request = requests.get(url=f"https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?serietype=line&apikey={fmp_api_key}")
    response = request.json()
    df = pd.json_normalize(response, 'historical')
    df = df.rename(columns={'date': 'Date', 'close': 'Close'})

    # Drop duplicates
    df = df.drop_duplicates(subset='Date')
    
    # Convert the 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Fill in missing dates with the value of the previous date
    df = df.set_index('Date').asfreq('D', method='bfill').reset_index()
    
    # Change the date format to DD/MM/YYYY
    df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')
    
    return df

