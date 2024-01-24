import streamlit as st
import json

# Load JSON data from file
with open('upstox_data.json', 'r') as file:
    data = json.load(file)

# Extract relevant data
strike_data = data['data']['strategyChainData']['strikeMap']

# Display the table using Streamlit
st.title('Option Chain Data')
st.write("Showing 'callOptionData' and 'putOptionData' for all strikes with sentiment conditions.")

# Table header
columns = ['Strike', 'Option Type', 'Instrument Key', 'LTP', 'Bid Price', 'Bid Qty', 'Ask Price', 'Ask Qty', 'Volume', 'OI', 'Prev OI', 'OI Change', 'Sentiment', 'Trend', 'Delta', 'Gamma', 'Vega', 'Theta', 'IV', 'PCR', 'Sentiment Condition']
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
    oi_call = market_data_call.get('oi', 0)
    prev_oi_call = market_data_call.get('prevOi', 0)
    oi_change_call = oi_call - prev_oi_call
    sentiment_call = 'Bullish' if oi_change_call > 0 else 'Bearish' if oi_change_call < 0 else 'Neutral'
    
    # Determine trend for Call Option
    volume_call = market_data_call.get('volume', 0)
    trend_call = 'Day Trend' if volume_call > 0 and oi_call <= volume_call else 'Long-Term Trend' if volume_call > 0 and oi_call > volume_call else 'No Trend'
    
    # Extract relevant analytics data
    delta_call = analytics_call.get('delta', 0)
    gamma_call = analytics_call.get('gamma', 0)
    vega_call = analytics_call.get('vega', 0)
    theta_call = analytics_call.get('theta', 0)
    iv_call = analytics_call.get('iv', 0)

    # Determine sentiment based on conditions
    if delta_call >= 0.7 and gamma_call >= 0.7 and vega_call > 0 and theta_call <= 0 and iv_call > 0 and oi_change_call > 0:
        sentiment_condition_call = 'Strong Bullish'
    elif 0.3 <= delta_call < 0.7 and 0.3 <= gamma_call < 0.7 and vega_call >= 0 and theta_call >= 0 and (iv_call >= 0 or oi_change_call > 0):
        sentiment_condition_call = 'Mild Bullish'
    elif -0.3 <= delta_call <= 0.3 and 0 <= gamma_call <= 0.3 and vega_call == 0 and -0.3 <= theta_call <= 0.3 and iv_call == 0 and oi_change_call == 0:
        sentiment_condition_call = 'Neutral'
    elif -0.7 <= delta_call < -0.3 and 0 <= gamma_call <= 0.7 and vega_call >= 0 and -0.3 <= theta_call <= 0 and (iv_call >= 0 or oi_change_call > 0):
        sentiment_condition_call = 'Mild Bearish'
    elif delta_call < -0.7 and gamma_call >= 0.7 and vega_call > 0 and theta_call >= 0 and iv_call > 0 and oi_change_call > 0:
        sentiment_condition_call = 'Strong Bearish'
    else:
        sentiment_condition_call = 'Not Defined'

    row_call = [strike, 'Call', instrument_key_call, market_data_call.get('ltp', 0), market_data_call.get('bidPrice', 0), market_data_call.get('bidQty', 0),
           market_data_call.get('askPrice', 0), market_data_call.get('askQty', 0), volume_call, oi_call, prev_oi_call, oi_change_call,
           sentiment_call, trend_call, delta_call, gamma_call, vega_call, theta_call, iv_call, pcr_call, sentiment_condition_call]
    
    table_data.append(row_call)
    
    # Add Put Option Data
    instrument_key_put = put_data.get('instrumentKey', '')
    market_data_put = put_data.get('marketData', {})
    analytics_put = put_data.get('analytics', {})
    pcr_put = strike_info.get('pcr', None)
    oi_put = market_data_put.get('oi', 0)
    prev_oi_put = market_data_put.get('prevOi', 0)
    oi_change_put = oi_put - prev_oi_put
    sentiment_put = 'Bullish' if oi_change_put > 0 else 'Bearish' if oi_change_put < 0 else 'Neutral'
    
    # Determine trend for Put Option
    volume_put = market_data_put.get('volume', 0)
    trend_put = 'Day Trend' if volume_put > 0 and oi_put <= volume_put else 'Long-Term Trend' if volume_put > 0 and oi_put > volume_put else 'No Trend'
    
    # Extract relevant analytics data
    delta_put = analytics_put.get('delta', 0)
    gamma_put = analytics_put.get('gamma', 0)
    vega_put = analytics_put.get('vega', 0)
    theta_put = analytics_put.get('theta', 0)
    iv_put = analytics_put.get('iv', 0)

    # Determine sentiment based on conditions
    if delta_put >= 0.7 and gamma_put >= 0.7 and vega_put > 0 and theta_put >= 0 and iv_put > 0 and oi_change_put > 0:
        sentiment_condition_put = 'Strong Bullish'
    elif 0.3 <= delta_put < 0.7 and 0.3 <= gamma_put < 0.7 and vega_put >= 0 and theta_put >= 0 and (iv_put >= 0 or oi_change_put > 0):
        sentiment_condition_put = 'Mild Bullish'
    elif -0.3 <= delta_put <= 0.3 and 0 <= gamma_put <= 0.3 and vega_put == 0 and -0.3 <= theta_put <= 0.3 and iv_put == 0 and oi_change_put == 0:
        sentiment_condition_put = 'Neutral'
    elif -0.7 <= delta_put < -0.3 and 0 <= gamma_put <= 0.7 and vega_put >= 0 and -0.3 <= theta_put <= 0 and (iv_put >= 0 or oi_change_put > 0):
        sentiment_condition_put = 'Mild Bearish'
    elif delta_put < -0.7 and gamma_put >= 0.7 and vega_put > 0 and theta_put >= 0 and iv_put > 0 and oi_change_put > 0:
        sentiment_condition_put = 'Strong Bearish'
    else:
        sentiment_condition_put = 'Not Defined'

    row_put = [strike, 'Put', instrument_key_put, market_data_put.get('ltp', 0), market_data_put.get('bidPrice', 0), market_data_put.get('bidQty', 0),
           market_data_put.get('askPrice', 0), market_data_put.get('askQty', 0), volume_put, oi_put, prev_oi_put, oi_change_put,
           sentiment_put, trend_put, delta_put, gamma_put, vega_put, theta_put, iv_put, pcr_put, sentiment_condition_put]
    
    table_data.append(row_put)

# Display the table with headings
st.table([columns] + table_data)
