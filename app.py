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

    st.dataframe(pd.json_normalize(data))

    call_sum = sum(item['oi'] - item['prevOi'] for item in data['call'])
    put_sum = sum(item['oi'] - item['prevOi'] for item in data['put'])
    difference = call_sum - put_sum

    st.subheader("Options Open Interest Analysis")

    # Display the data in a table
    df_call = pd.DataFrame(data['call'])
    df_put = pd.DataFrame(data['put'])

    st.subheader("Call Options")
    st.dataframe(df_call)

    st.subheader("Put Options")
    st.dataframe(df_put)

    st.subheader("Summary")
    st.write(f"Call Sum: {call_sum}")
    st.write(f"Put Sum: {put_sum}")
    st.write(f"Difference: {difference}")

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
