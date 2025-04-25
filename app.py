import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")

st.markdown("This Application is a Streamlit Dashboard to Analyze the Sentiment of Tweets🐦")
st.sidebar.markdown("This Application is a Streamlit Dashboard to Analyze the Sentiment of Tweets🐦")


DATA_URL = "C:/Users/idial/Downloads/Cours Streamlit with Atom coursera/Projects twitter US Airline Sentiment/Projects/Tweets.csv"


st.cache_data(persist=True)
def load_data() :
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime( data['tweet_created'])
    return data


data = load_data()

st.write(data)

st.sidebar.subheader("Show Random Tweets")
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n = 1).iat[0,0])


st.sidebar.markdown("### Number of Tweets by Sentiment")
select= st.sidebar.selectbox('Visualization Type', ['Histogram', 'Pie Chart'], key = '1')
sentiment_count= data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})



if not st.sidebar.checkbox('Hide', True):
    st.markdown('### Number of Tweets by Sentiment')
    if select == 'Histogram':
        fig = px.bar(sentiment_count, x ='Sentiment', y ='Tweets', color ='Tweets', height = 500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, names ='Sentiment', values ='Tweets')
        st.plotly_chart(fig)




st.sidebar.subheader("When and where are Users Tweeting from?")
hour = st.sidebar.slider('Hour of day', 0, 23)
#hour = st.sidebar.number_input('Hour of day', min_value= 1, max_value=24)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key = '2'):                                                    #, key = '1'
    st.markdown('### Tweets Location Based on the Time of Day')
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour + 1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox('Show row data', False):
       st.write(modified_data)



st.sidebar.subheader("Breakdown Airline Tweets by Sentiment")
choice = st.sidebar.multiselect("Pick Airlines", ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key = '0')


if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x = 'airline', y = 'airline_sentiment', histfunc = 'count',
                               color = 'airline_sentiment', facet_col= 'airline_sentiment', labels= {'airline_sentiment':'tweets'}, height= 600, width= 800)
    st.plotly_chart(fig_choice)



st.sidebar.header('Word Cloud Sentiment')
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment', ('positive', 'neutral', 'negative'))

if not st.sidebar.checkbox("Close", True, key = '3'):
    st.header('Word Cloud for %s Sentiment' % (word_sentiment)) 
    df = data[data['airline_sentiment'] == word_sentiment]  
    words = ' ' .join(df['text'])   
    processed_words =   ' ' .join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])    
    word_cloud = WordCloud(stopwords= STOPWORDS, background_color= 'white', height= 640, width= 800).generate(processed_words)  
    plt.imshow(word_cloud)  
    plt.xticks([])
    plt.yticks([])
    st.set_option('deprecation.showPyplotGlobalUse', False)  
    st.pyplot()                                   
   







