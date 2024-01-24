import streamlit as st
import json

# Define the threshold values
threshold_high = 1000  # You can adjust this value based on your analysis
threshold_low = 500    # You can adjust this value based on your analysis

# Load JSON data from file
with open('upstox_data.json', 'r') as file:
    data = json.load(file)

# Extract relevant data
strike_data = data['data']['strategyChainData']['strikeMap']

# Display the table using Streamlit
st.title('Option Chain Data Analysis')
st.write("Select a strike price to view detailed information for both call and put options.")

# Dropdown to select the strike price
selected_strike = st.selectbox('Select Strike Price', list(map(float, strike_data.keys())))

# Table header
columns = ['Option Type', 'Instrument Key', 'LTP', 'Bid Price', 'Bid Qty', 'Ask Price', 'Ask Qty', 'Volume', 'OI', 'Prev OI', 'OI Change',
           'Sentiment', 'Trend', 'Delta', 'Gamma', 'Vega', 'Theta', 'IV', 'PCR', 'Sentiment Condition', 'Vol OI Analysis']
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

# New condition for Vol OI Analysis
vol_oi_analysis_call = ''
if volume_call > threshold_high and oi_change_call > 0:
    vol_oi_analysis_call = 'Strong Trend: High Volume and Increasing Open Interest'
elif (volume_call > threshold_high and oi_change_call < 0) or (volume_call < threshold_low and oi_change_call > 0):
    vol_oi_analysis_call = 'Potential Reversal: Divergences Between Volume and Open Interest'
else:
    vol_oi_analysis_call = 'No Clear Signal'

# Add data to the table
row_call = ['Call', instrument_key_call, market_data_call.get('ltp', 0), market_data_call.get('bidPrice', 0), market_data_call.get('bidQty', 0),
            market_data_call.get('askPrice', 0), market_data_call.get('askQty', 0), volume_call, oi_call, prev_oi_call, oi_change_call,
            sentiment_call, trend_call, delta_call, gamma_call, vega_call, theta_call, iv_call, pcr_call, sentiment_condition_call, vol_oi_analysis_call]

table_data.append(row_call)

# Put Option Data (similar modifications as for Call Option Data)

# Display the table with headings
st.table([columns] + table_data)
