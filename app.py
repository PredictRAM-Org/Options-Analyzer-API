import streamlit as st
import requests

# Function to fetch option data based on strikeMap
def fetch_option_data(strike_map):
    api_url = f"https://service.upstox.com/option-analytics-tool/open/v1/strategy-chains?assetKey=NSE_INDEX%7CNifty+50&strategyChainType=PC_CHAIN&expiry=25-01-2024"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        option_data = response.json()

        # Check the structure of the API response
        print(option_data)

        # Filter data based on selected strikeMap
        call_option_data = [option for option in option_data.get('callOptionData', []) if option.get('strikePrice') == strike_map]
        put_option_data = [option for option in option_data.get('putOptionData', []) if option.get('strikePrice') == strike_map]
        
        market_data = option_data.get('marketData', {})

        return call_option_data, put_option_data, market_data
    else:
        st.error(f"Error fetching data. Status Code: {response.status_code}")
        return None, None, None

# Streamlit app
def main():
    st.title("Option Analytics App")
    
    # Option to select strikeMap
    selected_strike_map = st.selectbox("Select StrikeMap:", [20000, 20050, 20100])
    
    # Fetch option data based on selected strikeMap
    call_options, put_options, market_data = fetch_option_data(selected_strike_map)
    
    # Display call option data in a table
    st.subheader("Call Option Data")
    if call_options:
        st.table(call_options)
    else:
        st.warning("No data available for selected strikeMap.")

    # Display put option data in a table
    st.subheader("Put Option Data")
    if put_options:
        st.table(put_options)
    else:
        st.warning("No data available for selected strikeMap.")

    # Display market data
    st.subheader("Market Data")
    st.write(f"Open Interest (OI): {market_data.get('oi', 'N/A')}")
    st.write(f"Change in OI: {market_data.get('changeInOI', 'N/A')}")
    st.write(f"Volume: {market_data.get('volume', 'N/A')}")
    st.write(f"Change in Volume: {market_data.get('changeInVolume', 'N/A')}")

if __name__ == "__main__":
    main()
