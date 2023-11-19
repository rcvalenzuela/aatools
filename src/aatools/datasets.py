
import pandas as pd

def load_transport():
    "Loads the transport dataset"
    
    transport_url = 'https://raw.githubusercontent.com/rcvalenzuela/aatools-data/main/transport.csv'
    transport = pd.read_csv(transport_url, sep=';')
    transport = transport.drop(['num'], axis=1)
    
    return transport


def load_predictions():
    "Loads the transport dataset"
    
    df_url = 'https://raw.githubusercontent.com/rcvalenzuela/aatools-data/main/predictions.csv'
    df = pd.read_csv(df_url, sep=',')
    
    return df