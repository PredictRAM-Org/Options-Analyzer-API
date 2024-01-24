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

    # Display the strike map in the center
    st.write("---")
    st.subheader("Strike Map")
    st.write("Center Column - Strike Map")
    st.write("---")

    # Display the call options on the left
    st.write("---")
    st.subheader("Call Options")
    st.table(pd.DataFrame(call_data))
    st.write("---")

    # Display the put options on the right
    st.write("---")
    st.subheader("Put Options")
    st.table(pd.DataFrame(put_data))
    st.write("---")

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
