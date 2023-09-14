import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import streamlit as st

from src.news_sentiment import latest_news
from src.utils import round_numeric

st.set_page_config(page_title='News Sentiment Analysis', page_icon=':newspaper:', layout='wide')

st.title('News Sentiment Analysis')

st.write('This app shows the sentiment of the latest news articles about a company.')

ticker = st.text_input('Enter a ticker symbol')


if "latest_news" not in st.session_state:
    st.session_state.latest_news = None

if st.button('Get Data'):
    with st.spinner('Getting latest news...'):
        st.session_state.latest_news = latest_news(ticker, 10)



if st.session_state.latest_news:

    st.markdown("## Latest News")

    column_config = {
            "title": st.column_config.Column(
                "Title",
                width="large",
            ),
            "url": st.column_config.LinkColumn(
                "Link",
                width="medium",
            ),
            "authors": st.column_config.ListColumn(
                "Authors",
                width = "medium"
            ),
            "topics": st.column_config.ListColumn(
                "Topics",
                width="large"
            ),
            "sentiment_score" : st.column_config.ProgressColumn(
                "Sentiment Score",
                min_value=-0.5,
                max_value=0.5
            ),
            "sentiment_label": st.column_config.Column(
               "Sentiment Label" 
            )

        }

    st.metric("Mean Sentiment Score", 
              value=round_numeric(st.session_state.latest_news["mean_sentiment_score"]), 
              delta=st.session_state.latest_news["mean_sentiment_class"])
    
    st.dataframe(st.session_state.latest_news["news"], column_config=column_config)



