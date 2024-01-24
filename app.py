import requests
import json
import streamlit as st

# Function to fetch data from the API and save it to a JSON file
def fetch_and_save_data(api_url, file_path):
    response = requests.get(api_url)
    data = response.json()

    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

# Function to analyze options data
def analyze_options_data(data):
    call_sum = 0
    put_sum = 0

    # Loop through the data and calculate sums
    for strategy_chain in data.get('data', []):
        for leg in strategy_chain.get('legs', []):
            if leg.get('optionType') == 'CE':  # Call option
                call_sum += leg.get('changeinOpenInterest', 0)
            elif leg.get('optionType') == 'PE':  # Put option
                put_sum += leg.get('changeinOpenInterest', 0)

    # Display results
    st.write("**Call Sum:**", call_sum)
    st.write("**Put Sum:**", put_sum)

# Main Streamlit app
def main():
    st.title("Options Analyzer App")

    # Fetch and save data on button click
    if st.button("Fetch and Save Options Data"):
        api_url = "https://service.upstox.com/option-analytics-tool/open/v1/strategy-chains?assetKey=NSE_INDEX%7CNifty+50&strategyChainType=PC_CHAIN&expiry=25-01-2024"
        file_path = "options_data.json"
        fetch_and_save_data(api_url, file_path)
        st.success("Options data successfully fetched and saved.")

    # Load options data from the saved JSON file
    file_path = "options_data.json"
    try:
        with open(file_path, 'r') as json_file:
            options_data = json.load(json_file)

        # Analyze options data
        analyze_options_data(options_data)

    except FileNotFoundError:
        st.warning("Options data not found. Please fetch and save data first.")

if __name__ == "__main__":
    main()
