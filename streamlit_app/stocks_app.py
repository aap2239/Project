import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime

# Function to fetch historical stock data
def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Function to load tweets from CSV file
def load_tweets(csv_file):
    return pd.read_csv(csv_file)

tweets_csv = "/home/aishpats/Documents/Columbia_MS_EE/Spring_2023/Large_Scale_Stream_Processing/Project/data/datafiles_twdata (2).csv"
tweets_df = load_tweets(tweets_csv)
print(tweets_df)
# Sidebar
st.sidebar.title("Select a Company")
company = st.sidebar.selectbox("Choose a company", ("Apple", "Google", "Microsoft"))

# Map company names to their ticker symbols
ticker_map = {"Apple": "AAPL", "Google": "GOOGL", "Microsoft": "MSFT"}

# Get the historical stock data
start_date = "2020-01-01"
end_date = datetime.now().strftime("%Y-%m-%d")
stock_data = get_stock_data(ticker_map[company], start_date, end_date)

# Main title
st.title(f"{company} Stock Market Trends")

# Display historical stock prices timeseries line chart
st.header("Historical Stock Prices")
fig = px.line(stock_data, x=stock_data.index, y="Close", labels={"x": "Date", "y": "Close Price"})
st.plotly_chart(fig)

# Load and display live tweets
st.header("Live Tweets")


# Filter tweets for the selected company
filtered_tweets = tweets_df[tweets_df["Stocks"] == company]

# Display the latest 10 tweets
for index, tweet in filtered_tweets.tail(10).iterrows():
    st.write(f"{tweet['Date']} : {tweet['Tweet']}")