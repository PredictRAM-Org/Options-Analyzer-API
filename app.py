import streamlit as st
import json
import pandas as pd

# Define the threshold values
threshold_high = 5000000  # You can adjust this value based on your analysis
threshold_low = 1000000    # You can adjust this value based on your analysis

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

# Simplified column names for better display
columns = [
    'Option Type', 'LTP', 'Bid Price', 'Bid Qty', 'Ask Price', 'Ask Qty', 
    'Volume', 'OI', 'OI Change', 'Sentiment', 'Trend', 'Delta',
    'IV', 'PCR', 'Vol-OI Analysis', 'Call Sum', 'Put Sum', 'Flow Diff'
]

# Mapping between original and simplified column names
column_mapping = {
    'Option Type': 'Option Type',
    'Instrument Key': 'Instrument Key',
    'LTP': 'LTP',
    'Bid Price': 'Bid Price',
    'Bid Qty': 'Bid Qty',
    'Ask Price': 'Ask Price',
    'Ask Qty': 'Ask Qty',
    'Volume': 'Volume',
    'OI': 'OI',
    'Prev OI': 'Prev OI',
    'OI Change': 'OI Change',
    'Call OI Change | Calculated': 'Call OI Change',
    'Put OI Change | Calculated': 'Put OI Change',
    'Total Call Change in OI': 'Total Call ΔOI',
    'Total Put Change in OI': 'Total Put ΔOI',
    'Sentiment': 'Sentiment',
    'Trend': 'Trend',
    'Delta': 'Delta',
    'Gamma': 'Gamma',
    'Vega': 'Vega',
    'Theta': 'Theta',
    'IV': 'IV',
    'PCR': 'PCR',
    'Sentiment Condition': 'Sentiment Cond',
    'Vol OI Analysis': 'Vol-OI Analysis',
    'Call Sum | Calculated': 'Call Sum',
    'Put Sum | Calculated': 'Put Sum',
    'Options Flow Diff | Calculated': 'Flow Diff'
}

table_data = []

# Populate the table with data for the selected strike
strike_info = strike_data[str(selected_strike)]

# Call Option Data
call_data = strike_info.get('callOptionData', {})
market_data_call = call_data.get('marketData', {})
oi_call = market_data_call.get('oi', 0)
prev_oi_call = market_data_call.get('prevOi', 0)
oi_change_call = oi_call - prev_oi_call
volume_call = market_data_call.get('volume', 0)
delta_call = call_data.get('analytics', {}).get('delta', 0)

# Vol OI Analysis for Call
vol_oi_analysis_call = ''
if volume_call > threshold_high and oi_change_call > 0:
    vol_oi_analysis_call = 'Strong Trend'
elif (volume_call > threshold_high and oi_change_call < 0) or (volume_call < threshold_low and oi_change_call > 0):
    vol_oi_analysis_call = 'Potential Reversal'
else:
    vol_oi_analysis_call = 'No Clear Signal'

# Calculate Call Sum
call_sum_calculated = 0
for i in range(int(selected_strike), int(selected_strike) - 5, -1):
    if str(i) in strike_data:
        call_sum_calculated += strike_data[str(i)].get('callOptionData', {}).get('marketData', {}).get('oi', 0) - strike_data[str(i)].get('callOptionData', {}).get('marketData', {}).get('prevOi', 0)

# Put Option Data
put_data = strike_info.get('putOptionData', {})
market_data_put = put_data.get('marketData', {})
oi_put = market_data_put.get('oi', 0)
prev_oi_put = market_data_put.get('prevOi', 0)
oi_change_put = oi_put - prev_oi_put
volume_put = market_data_put.get('volume', 0)
delta_put = put_data.get('analytics', {}).get('delta', 0)

# Vol OI Analysis for Put
vol_oi_analysis_put = ''
if volume_put > threshold_high and oi_change_put > 0:
    vol_oi_analysis_put = 'Strong Trend'
elif (volume_put > threshold_high and oi_change_put < 0) or (volume_put < threshold_low and oi_change_put > 0):
    vol_oi_analysis_put = 'Potential Reversal'
else:
    vol_oi_analysis_put = 'No Clear Signal'

# Calculate Put Sum
put_sum_calculated = 0
for i in range(int(selected_strike), int(selected_strike) + 5):
    if str(i) in strike_data:
        put_sum_calculated += strike_data[str(i)].get('putOptionData', {}).get('marketData', {}).get('oi', 0) - strike_data[str(i)].get('putOptionData', {}).get('marketData', {}).get('prevOi', 0)

# Calculate Options Flow Difference
options_flow_diff_calculated = call_sum_calculated - put_sum_calculated

# Create DataFrame for better display
df = pd.DataFrame(columns=columns)

# Add Call data
df.loc['Call'] = [
    'Call',
    market_data_call.get('ltp', 0),
    market_data_call.get('bidPrice', 0),
    market_data_call.get('bidQty', 0),
    market_data_call.get('askPrice', 0),
    market_data_call.get('askQty', 0),
    volume_call,
    oi_call,
    oi_change_call,
    'Bullish' if oi_change_call > 0 else 'Bearish' if oi_change_call < 0 else 'Neutral',
    'Day Trend' if volume_call > 0 and oi_call <= volume_call else 'Long-Term' if volume_call > 0 and oi_call > volume_call else 'No Trend',
    delta_call,
    call_data.get('analytics', {}).get('iv', 0),
    strike_info.get('pcr', None),
    vol_oi_analysis_call,
    call_sum_calculated,
    put_sum_calculated,
    options_flow_diff_calculated
]

# Add Put data
df.loc['Put'] = [
    'Put',
    market_data_put.get('ltp', 0),
    market_data_put.get('bidPrice', 0),
    market_data_put.get('bidQty', 0),
    market_data_put.get('askPrice', 0),
    market_data_put.get('askQty', 0),
    volume_put,
    oi_put,
    oi_change_put,
    'Bullish' if oi_change_put > 0 else 'Bearish' if oi_change_put < 0 else 'Neutral',
    'Day Trend' if volume_put > 0 and oi_put <= volume_put else 'Long-Term' if volume_put > 0 and oi_put > volume_put else 'No Trend',
    delta_put,
    put_data.get('analytics', {}).get('iv', 0),
    strike_info.get('pcr', None),
    vol_oi_analysis_put,
    call_sum_calculated,
    put_sum_calculated,
    options_flow_diff_calculated
]

# Format numeric columns
numeric_cols = ['LTP', 'Bid Price', 'Ask Price', 'Volume', 'OI', 'OI Change', 'Delta', 'IV', 'Call Sum', 'Put Sum', 'Flow Diff']
df[numeric_cols] = df[numeric_cols].applymap(lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else x)

# Display the table
st.dataframe(df.style
    .set_properties(**{'text-align': 'center'})
    .set_table_styles([{
        'selector': 'th',
        'props': [('text-align', 'center')]
    }]), 
    use_container_width=True)

# Add some metrics at the top
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("PCR", f"{strike_info.get('pcr', 0):.2f}")
with col2:
    st.metric("Call OI Change", f"{oi_change_call:,}")
with col3:
    st.metric("Put OI Change", f"{oi_change_put:,}")

# Add interpretation
st.subheader("Interpretation")
if options_flow_diff_calculated > 0:
    st.warning("Options Flow Difference is positive (Call-heavy), suggesting potential bullish sentiment")
else:
    st.warning("Options Flow Difference is negative (Put-heavy), suggesting potential bearish sentiment")
