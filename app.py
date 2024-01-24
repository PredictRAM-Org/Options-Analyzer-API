import streamlit as st
import json

# Load JSON data from file
with open('upstox_data.json', 'r') as file:
    data = json.load(file)

# Extract relevant data
strike_data = data['data']['strategyChainData']['strikeMap']

# Display the table using Streamlit
st.title('Option Chain Data Analysis')
st.write("Select a strike price to view detailed information for both call and put options.")

# Slider to select the strike price
selected_strike = st.slider('Select Strike Price', min_value=min(strike_data.keys()), max_value=max(strike_data.keys()))

# Table header
columns = ['Option Type', 'Instrument Key', 'LTP', 'Bid Price', 'Bid Qty', 'Ask Price', 'Ask Qty', 'Volume', 'OI', 'Prev OI', 'OI Change', 'Sentiment', 'Trend', 'Delta', 'Gamma', 'Vega', 'Theta', 'IV', 'PCR', 'Sentiment Condition']
table_data = []

# Populate the table with data for the selected strike
strike_info = strike_data[str(selected_strike)]

# Call Option Data
call_data = strike_info.get('callOptionData', {})
instrument_key_call = call_data.get('instrumentKey', '')
market_data_call = call_data.get('marketData', {})
analytics_call = call_data.get('analytics', {})
oi_call = market_data_call.get('oi', 0)
prev_oi_call = market_data_call.get('prevOi', 0)
oi_change_call = oi_call - prev_oi_call
sentiment_call = 'Bullish' if oi_change_call > 0 else 'Bearish' if oi_change_call < 0 else 'Neutral'
volume_call = market_data_call.get('volume', 0)
trend_call = 'Day Trend' if volume_call > 0 and oi_call <= volume_call else 'Long-Term Trend' if volume_call > 0 and oi_call > volume_call else 'No Trend'
delta_call = analytics_call.get('delta', 0)
gamma_call = analytics_call.get('gamma', 0)
vega_call = analytics_call.get('vega', 0)
theta_call = analytics_call.get('theta', 0)
iv_call = analytics_call.get('iv', 0)
pcr_call = strike_info.get('pcr', None)
sentiment_condition_call = 'Not Defined'  # You can add conditions based on user preferences

# Put Option Data
put_data = strike_info.get('putOptionData', {})
instrument_key_put = put_data.get('instrumentKey', '')
market_data_put = put_data.get('marketData', {})
analytics_put = put_data.get('analytics', {})
oi_put = market_data_put.get('oi', 0)
prev_oi_put = market_data_put.get('prevOi', 0)
oi_change_put = oi_put - prev_oi_put
sentiment_put = 'Bullish' if oi_change_put > 0 else 'Bearish' if oi_change_put < 0 else 'Neutral'
volume_put = market_data_put.get('volume', 0)
trend_put = 'Day Trend' if volume_put > 0 and oi_put <= volume_put else 'Long-Term Trend' if volume_put > 0 and oi_put > volume_put else 'No Trend'
delta_put = analytics_put.get('delta', 0)
gamma_put = analytics_put.get('gamma', 0)
vega_put = analytics_put.get('vega', 0)
theta_put = analytics_put.get('theta', 0)
iv_put = analytics_put.get('iv', 0)
pcr_put = strike_info.get('pcr', None)
sentiment_condition_put = 'Not Defined'  # You can add conditions based on user preferences

# Add data to the table
row_call = ['Call', instrument_key_call, market_data_call.get('ltp', 0), market_data_call.get('bidPrice', 0), market_data_call.get('bidQty', 0),
            market_data_call.get('askPrice', 0), market_data_call.get('askQty', 0), volume_call, oi_call, prev_oi_call, oi_change_call,
            sentiment_call, trend_call, delta_call, gamma_call, vega_call, theta_call, iv_call, pcr_call, sentiment_condition_call]
row_put = ['Put', instrument_key_put, market_data_put.get('ltp', 0), market_data_put.get('bidPrice', 0), market_data_put.get('bidQty', 0),
           market_data_put.get('askPrice', 0), market_data_put.get('askQty', 0), volume_put, oi_put, prev_oi_put, oi_change_put,
           sentiment_put, trend_put, delta_put, gamma_put, vega_put, theta_put, iv_put, pcr_put, sentiment_condition_put]

table_data.extend([row_call, row_put])

# Display the table with headings
st.table([columns] + table_data)
