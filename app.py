import streamlit as st
import json

# Load JSON data from file
with open('upstox_data.json', 'r') as file:
    data = json.load(file)

# Extract relevant data
strike_data = data['data']['strategyChainData']['strikeMap']

# Display the table using Streamlit
st.title('Option Chain Data')
st.write("Showing 'callOptionData' and 'putOptionData' for all strikes in a table format.")

# Table header
columns = ['Strike', 'Option Type', 'Instrument Key', 'LTP', 'Bid Price', 'Bid Qty', 'Ask Price', 'Ask Qty', 'Volume', 'OI', 'Prev OI', 'Vega', 'Theta', 'Gamma', 'Delta', 'IV', 'PCR']
table_data = []

# Populate the table with data
for strike, strike_info in strike_data.items():
    call_data = strike_info.get('callOptionData', {})
    put_data = strike_info.get('putOptionData', {})
    
    # Add Call Option Data
    instrument_key_call = call_data.get('instrumentKey', '')
    market_data_call = call_data.get('marketData', {})
    analytics_call = call_data.get('analytics', {})
    pcr_call = strike_info.get('pcr', None)

    row_call = [strike, 'Call', instrument_key_call, market_data_call.get('ltp', 0), market_data_call.get('bidPrice', 0), market_data_call.get('bidQty', 0),
           market_data_call.get('askPrice', 0), market_data_call.get('askQty', 0), market_data_call.get('volume', 0), market_data_call.get('oi', 0),
           market_data_call.get('prevOi', 0), analytics_call.get('vega', 0), analytics_call.get('theta', 0), analytics_call.get('gamma', 0), analytics_call.get('delta', 0),
           analytics_call.get('iv', 0), pcr_call]
    
    table_data.append(row_call)
    
    # Add Put Option Data
    instrument_key_put = put_data.get('instrumentKey', '')
    market_data_put = put_data.get('marketData', {})
    analytics_put = put_data.get('analytics', {})
    pcr_put = strike_info.get('pcr', None)

    row_put = [strike, 'Put', instrument_key_put, market_data_put.get('ltp', 0), market_data_put.get('bidPrice', 0), market_data_put.get('bidQty', 0),
           market_data_put.get('askPrice', 0), market_data_put.get('askQty', 0), market_data_put.get('volume', 0), market_data_put.get('oi', 0),
           market_data_put.get('prevOi', 0), analytics_put.get('vega', 0), analytics_put.get('theta', 0), analytics_put.get('gamma', 0), analytics_put.get('delta', 0),
           analytics_put.get('iv', 0), pcr_put]
    
    table_data.append(row_put)

# Display the table with headings
st.table([columns] + table_data)
