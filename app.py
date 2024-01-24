import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

# Function to fetch options data from the API
def fetch_options_data():
    api_url = "https://service.upstox.com/option-analytics-tool/open/v1/strategy-chains?assetKey=NSE_INDEX%7CNifty+50&strategyChainType=PC_CHAIN&expiry=25-01-2024"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data.get('strikeMap', {})
    else:
        st.error(f"Error fetching data from API. Status code: {response.status_code}")
        return {}

# Function to analyze options chain
def analyze_options_chain(call_strike, put_strike, options_data):
    # Extract call and put option data
    call_option_data = options_data.get('callOptionData', {}).get(str(call_strike), {})
    put_option_data = options_data.get('putOptionData', {}).get(str(put_strike), {})

    # Debug prints to identify the issue
    print(f"Selected Call Strike: {call_strike}, Call Option Data: {call_option_data}")
    print(f"Selected Put Strike: {put_strike}, Put Option Data: {put_option_data}")

    # Check if the required data is present
    if not call_option_data or not put_option_data:
        st.error(f"Error: Options data not found for the selected strikes. Call Strike: {call_strike}, Put Strike: {put_strike}")
        return {}

    # Extract relevant information from call and put option data
    call_sum = call_option_data.get('marketData', {}).get('oi', 0)
    put_sum = put_option_data.get('marketData', {}).get('oi', 0)
    difference = call_sum - put_sum

    # Perform other calculations as needed...

    result = {
        'Call Sum': call_sum,
        'Put Sum': put_sum,
        'Difference': difference,
        # Add other results as needed...
    }

    return result

def main():
    st.image("png_2.3-removebg-preview.png", width=400)
    st.title("Options Chain Explorer App")

    # Fetch options data from the API
    options_data = fetch_options_data()

    # Get unique strike prices for call and put
    call_strike_options = sorted(options_data.get('callOptionData', {}).keys(), key=int)
    put_strike_options = sorted(options_data.get('putOptionData', {}).keys(), key=int)

    # User input for selecting CALLSTRIKEPRICE and PUTSTRIKEPRICE
    call_strike = st.selectbox("Select CALLSTRIKEPRICE:", call_strike_options)
    put_strike = st.selectbox("Select PUTSTRIKEPRICE:", put_strike_options)

    # Analyze options chain and display the result
    result = analyze_options_chain(call_strike, put_strike, options_data)

    # Display the result in tables
    st.subheader("Options Chain Analysis Result:")
    st.table(pd.DataFrame(result.items(), columns=['Metric', 'Value']))

    # README for the result table
    st.subheader("Result Table Explanation:")
    # Add explanation...

if __name__ == "__main__":
    main()
