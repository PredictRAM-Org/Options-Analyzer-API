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
           'Call OI Change | Calculated', 'Put OI Change | Calculated', 'Total Call Change in OI', 'Total Put Change in OI', 'Sentiment', 'Trend', 'Delta',
           'Gamma', 'Vega', 'Theta', 'IV', 'PCR', 'Sentiment Condition', 'Vol OI Analysis', 'Call Sum | Calculated', 'Put Sum | Calculated',
           'Options Flow Diff | Calculated']
table_data = []

# Populate the table with data for the selected strike
strike_info = strike_data[str(selected_strike)]

# Call Option Data
call_data = strike_info.get('callOptionData', {})
instrument_key_call = call_data.get('instrumentKey', '')
market_data_call = call_data.get('marketData', {})
oi_call = market_data_call.get('oi', 0)
prev_oi_call = market_data_call.get('prevOi', 0)
oi_change_call = oi_call - prev_oi_call
volume_call = market_data_call.get('volume', 0)
delta_call = call_data.get('analytics', {}).get('delta', 0)

# New condition for Vol OI Analysis
vol_oi_analysis_call = ''
if volume_call > threshold_high and oi_change_call > 0:
    vol_oi_analysis_call = 'Strong Trend: High Volume and Increasing Open Interest'
elif (volume_call > threshold_high and oi_change_call < 0) or (volume_call < threshold_low and oi_change_call > 0):
    vol_oi_analysis_call = 'Potential Reversal: Divergences Between Volume and Open Interest'
else:
    vol_oi_analysis_call = 'No Clear Signal'

# Calculate Call Sum | Calculated
call_sum_calculated = 0
for i in range(int(selected_strike), int(selected_strike) - 5, -1):
    if str(i) in strike_data:
        call_sum_calculated += strike_data[str(i)].get('callOptionData', {}).get('marketData', {}).get('oi', 0) - strike_data[str(i)].get('callOptionData', {}).get('marketData', {}).get('prevOi', 0)

# Add data to the table for Call Option
row_call = ['Call', instrument_key_call, market_data_call.get('ltp', 0), market_data_call.get('bidPrice', 0), market_data_call.get('bidQty', 0),
            market_data_call.get('askPrice', 0), market_data_call.get('askQty', 0), volume_call, oi_call, prev_oi_call, oi_change_call,
            0, 0,  # Initialize Call OI Change and Put OI Change to 0
            0, 0,  # Initialize Total Call Change in OI and Total Put Change in OI to 0
            'Bullish' if oi_change_call > 0 else 'Bearish' if oi_change_call < 0 else 'Neutral',
            'Day Trend' if volume_call > 0 and oi_call <= volume_call else 'Long-Term Trend' if volume_call > 0 and oi_call > volume_call else 'No Trend',
            delta_call, call_data.get('analytics', {}).get('gamma', 0), call_data.get('analytics', {}).get('vega', 0), call_data.get('analytics', {}).get('theta', 0),
            call_data.get('analytics', {}).get('iv', 0), strike_info.get('pcr', None), 'Not Defined', vol_oi_analysis_call,
            call_sum_calculated, 0, 0]  # Initialize Put Sum and Options Flow Diff to 0

table_data.append(row_call)

# Put Option Data
put_data = strike_info.get('putOptionData', {})
instrument_key_put = put_data.get('instrumentKey', '')
market_data_put = put_data.get('marketData', {})
oi_put = market_data_put.get('oi', 0)
prev_oi_put = market_data_put.get('prevOi', 0)
oi_change_put = oi_put - prev_oi_put
volume_put = market_data_put.get('volume', 0)
delta_put = put_data.get('analytics', {}).get('delta', 0)

# New condition for Vol OI Analysis for Put Option
vol_oi_analysis_put = ''
if volume_put > threshold_high and oi_change_put > 0:
    vol_oi_analysis_put = 'Strong Trend: High Volume and Increasing Open Interest'
elif (volume_put > threshold_high and oi_change_put < 0) or (volume_put < threshold_low and oi_change_put > 0):
    vol_oi_analysis_put = 'Potential Reversal: Divergences Between Volume and Open Interest'
else:
    vol_oi_analysis_put = 'No Clear Signal'

# Calculate Put Sum | Calculated
put_sum_calculated = 0
for i in range(int(selected_strike), int(selected_strike) + 5):
    if str(i) in strike_data:
        put_sum_calculated += strike_data[str(i)].get('putOptionData', {}).get('marketData', {}).get('oi', 0) - strike_data[str(i)].get('putOptionData', {}).get('marketData', {}).get('prevOi', 0)

# Calculate Options Flow Difference Analysis | Calculated
options_flow_diff_calculated = call_sum_calculated - put_sum_calculated

# Add data to the table for Put Option
row_put = ['Put', instrument_key_put, market_data_put.get('ltp', 0), market_data_put.get('bidPrice', 0), market_data_put.get('bidQty', 0),
           market_data_put.get('askPrice', 0), market_data_put.get('askQty', 0), volume_put, oi_put, prev_oi_put, oi_change_put,
           0, 0,  # Initialize Call OI Change and Put OI Change to 0
           0, 0,  # Initialize Total Call Change in OI and Total Put Change in OI to 0
           'Bullish' if oi_change_put > 0 else 'Bearish' if oi_change_put < 0 else 'Neutral',
           'Day Trend' if volume_put > 0 and oi_put <= volume_put else 'Long-Term Trend' if volume_put > 0 and oi_put > volume_put else 'No Trend',
           delta_put, put_data.get('analytics', {}).get('gamma', 0), put_data.get('analytics', {}).get('vega', 0), put_data.get('analytics', {}).get('theta', 0),
           put_data.get('analytics', {}).get('iv', 0), strike_info.get('pcr', None), 'Not Defined', vol_oi_analysis_put,
           0, put_sum_calculated, options_flow_diff_calculated]

table_data.append(row_put)

# Display the table with headings
st.table([columns] + table_data)
