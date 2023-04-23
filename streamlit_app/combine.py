import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from wordcloud import WordCloud
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Stock Analysis App", page_icon=":chart_with_upwards_trend:")
st.set_option('deprecation.showPyplotGlobalUse', False)

def get_stock_data(company):
    stock_data = pd.read_csv(r"C:\Users\Nupur\Downloads\dashboard_lssp-master\dashboard_lssp-master\data\data_historical (1).csv")
    stock_data = stock_data[stock_data["Company"] == company]
    return stock_data

def display_stock_line_graph(company):
    stock_data = get_stock_data(company)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['close'], name='close'))
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['open'], name='open'))
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['high'], name='high'))
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['low'], name='low'))

    fig.update_layout(title=f"{company} Stock Prices", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig)

def display_company_page():
    # Load news data from CSV file
    news_csv = "C:/Users/Nupur/Downloads/dashboard_lssp-master/dashboard_lssp-master/data/data_news_sentiments_2023-04-18-16-38-21.csv"
    if not os.path.isfile(news_csv):
        st.error("Error: Data file not found!")
        st.stop()

    news_df = pd.read_csv(news_csv)

    # Sidebar
    st.sidebar.title("Select a Company")
    companies = news_df["Company"].unique()
    company = st.sidebar.selectbox("Choose a company", companies)

    if company not in companies:
        st.error("Error: Company not found in the data!")
        st.stop()

    st.title(f"{company} Stock Analysis")
    display_stock_line_graph(company)

    # add additional analysis or information as needed
    st.write("Additional analysis or information goes here.")

    # Filter news for the selected company
    filtered_news = news_df[news_df["Company"] == company]
    # Filter news for the selected company

    company_logos = {
        "Apple": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
        "Google": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
        "Microsoft": "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg",
        "Amazon": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
        "Tesla": "https://upload.wikimedia.org/wikipedia/commons/b/bd/Tesla_Motors.svg",
        "AAPL": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
        "GOOGL": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
        "MSFT": "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg",
        "AMZN": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
        "TSLA": "https://upload.wikimedia.org/wikipedia/commons/b/bd/Tesla_Motors.svg"
    }
    # Display company logo
    st.sidebar.image(company_logos[company], use_column_width=True)

    # Main title and background color
    st.title(f"{company} News Dashboard")
  # Define the CSS style
    st.markdown("""
        <style>
            body {
                background-color: black;
            }
            .sidebar {
                background-color: white;
            }
        </style>
    """, unsafe_allow_html=True)
    st.header("Latest News Headlines")
    for index, news in filtered_news.head(10).iterrows():
        sentiment_color = "#FFFFFF"  # default to white for neutral sentiment
        if news['Sentiment'] == 'positive':
            sentiment_color = "#00FF00"  # green for positive sentiment
        elif news['Sentiment'] == 'negative':
            sentiment_color = "#FF0000"  # red for negative sentiment
        st.write(f"<div style='background-color:{sentiment_color}; padding:10px;'>{news['Date']} : {news['News']}</div>", unsafe_allow_html=True)
  

    # Generate word cloud for the selected company
    st.header("Word Cloud")
    text = " ".join(filtered_news['News'].astype(str).tolist())
    wordcloud = WordCloud().generate(text)
    st.image(wordcloud.to_array(), width=500, use_column_width=False)

    # Main title and background color
    st.title(f"{company} Twitter Dashboard")
    # Load data from CSV file
    tweets_df = pd.read_csv(r"C:\Users\Nupur\Downloads\dashboard_lssp-master\dashboard_lssp-master\data\datafiles_twdata (2).csv")


    # Filter data by selected company
    filtered_tweets = tweets_df[tweets_df["Company"] == company]

    # Display tweets table
    st.markdown(f"## {company} Tweets")
    st.dataframe(filtered_tweets[["ID", "Date", "Text"]])

    # Display sentiment analysis charts
    st.markdown(f"## {company} Sentiment Analysis")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=["Negative"], y=[filtered_tweets["Negative"].mean()], name="Negative"))
    fig.add_trace(go.Bar(x=["Neutral"], y=[filtered_tweets["Neutral"].mean()], name="Neutral"))
    fig.add_trace(go.Bar(x=["Positive"], y=[filtered_tweets["Positive"].mean()], name="Positive"))
    fig.update_layout(title=f"Sentiment Analysis for {company}")
    st.plotly_chart(fig)

    # Display word cloud with Twitter logo background shape
    st.markdown(f"## {company} Word Cloud")
    #text = " ".join(filtered_tweets["Text"].tolist())
    text = " ".join(filtered_tweets["Text"].astype(str).tolist())

    twitter_mask = np.array(Image.open(r"C:\Users\Nupur\Downloads\dashboard_lssp-master\dashboard_lssp-master\tests\twitter_mask.png"))
    wordcloud = WordCloud(mask=twitter_mask, background_color="white").generate(text)
    plt.figure(figsize=(10,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.margins(x=0, y=0)
    st.pyplot(plt.gcf()) # Pass the current figure to st.pyplot()


    # Hide Streamlit's menu and footer
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)



display_company_page()



   
