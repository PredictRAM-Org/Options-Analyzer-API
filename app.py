import streamlit as st
import requests
import pandas as pd

# Function to fetch data from the API
def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data. Status code: {response.status_code}")
        return None

# Function to process and display the data
def display_data(data):
    st.subheader("Raw Data:")
    if not data:
        st.error("Error: Invalid data format.")
        st.write("No data available.")
        return

    st.dataframe(pd.json_normalize(data), width=1000, height=400)

    st.subheader("Options Open Interest Analysis")

    # Separate call and put data
    call_data = data.get('call', [])
    put_data = data.get('put', [])

    # Display the strike map and data side by side
    st.write("---")
    st.subheader("Strike-wise Data")
    st.write("---")

    # Display header
    st.write("| Strike | Call Data | Put Data |")
    st.write("| ------ | --------- | --------- |")

    # Display data row-wise
    for strike, call, put in zip(call_data, put_data):
        st.write(f"| {strike['strikePrice']} | {call} | {put} |")

# Streamlit app
def main():
    st.title("Options Analytics Tool")
    
    # API link
    api_link = "https://service.upstox.com/option-analytics-tool/open/v1/strategy-chains?assetKey=NSE_INDEX%7CNifty+50&strategyChainType=PC_CHAIN&expiry=25-01-2024"
    
    # Fetch data from the API
    data = fetch_data(api_link)
    
    # Display data
    display_data(data)

if __name__ == "__main__":
    main()
