import streamlit as st
import json

# Load JSON data from file
with open('upstox_data.json', 'r') as file:
    data = json.load(file)

# Extract relevant data
strike_data = data['data']['strategyChainData']['strikeMap']

# Display the table using Streamlit
st.title('Option Chain Data')
st.write("Showing 'callOptionData' for all strikes in a table format.")

# Table header
columns = ['Strike', 'Instrument Key', 'LTP', 'Bid Price', 'Bid Qty', 'Ask Price', 'Ask Qty', 'Volume', 'OI', 'Prev OI', 'Vega', 'Theta', 'Gamma', 'Delta', 'IV', 'PCR']
table_data = []

# Populate the table with data
for strike, strike_info in strike_data.items():
    call_data = strike_info.get('callOptionData', {})
    instrument_key = call_data.get('instrumentKey', '')
    market_data = call_data.get('marketData', {})
    analytics = call_data.get('analytics', {})
    pcr = strike_info.get('pcr', None)

    row = [strike, instrument_key, market_data.get('ltp', 0), market_data.get('bidPrice', 0), market_data.get('bidQty', 0),
           market_data.get('askPrice', 0), market_data.get('askQty', 0), market_data.get('volume', 0), market_data.get('oi', 0),
           market_data.get('prevOi', 0), analytics.get('vega', 0), analytics.get('theta', 0), analytics.get('gamma', 0), analytics.get('delta', 0),
           analytics.get('iv', 0), pcr]

    table_data.append(row)

# Display the table
st.table(table_data)
