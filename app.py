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
    call_data = strike_info['callOptionData']
    instrument_key = call_data['instrumentKey']
    market_data = call_data['marketData']
    analytics = call_data['analytics']
    pcr = strike_info['pcr']

    row = [strike, instrument_key, market_data['ltp'], market_data['bidPrice'], market_data['bidQty'],
           market_data['askPrice'], market_data['askQty'], market_data['volume'], market_data['oi'],
           market_data['prevOi'], analytics['vega'], analytics['theta'], analytics['gamma'], analytics['delta'],
           analytics['iv'], pcr]

    table_data.append(row)

# Display the table
st.table(table_data)
