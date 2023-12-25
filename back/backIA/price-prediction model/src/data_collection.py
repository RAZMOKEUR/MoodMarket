import requests
import pandas as pd

fmp_api_key = "d3adc0ad134894b7b1bf044e468e5c69"


def get_nasdaq_constituent():
    # Make a GET request to fetch nasdaq constituent data
    nasdaq_constituent = requests.get(
        f"https://financialmodelingprep.com/api/v3/nasdaq_constituent?apikey={fmp_api_key}")
    df = pd.DataFrame(nasdaq_constituent.json())

    return df


def getstockpricehistory(stock):
    request = requests.get(
        url=f"https://financialmodelingprep.com/api/v3/historical-chart/1day/{stock}?apikey={fmp_api_key}")
    response = request.json()
    df = pd.json_normalize(response)

    # Drop duplicates
    df = df.drop_duplicates(subset='date')

    # Convert the 'Date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Fill in missing dates with the value of the previous date
    df = df.set_index('date').asfreq('D', method='bfill').reset_index()

    # Change the date format to DD/MM/YYYY
    df['date'] = df['date'].dt.strftime('%d/%m/%Y')

    return df
