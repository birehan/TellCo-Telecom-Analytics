
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import sys


script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(script_dir, "../")
sys.path.insert(0, parent_dir)
files_in_current_dir = os.listdir()

import utils as util

st.sidebar.header("Plotting Demo")

@st.cache_data()
def load_data():
    clean_data_df = pd.read_csv("data/cleaned_tellco_data.csv")
    return clean_data_df

@st.cache_data()
def load_eng_data():
    eng_data_df = pd.read_csv("data/tellco_user_engagement_data.csv")
    return eng_data_df

clean_data_df = load_data()
eng_data_df = load_eng_data()

def plotly_plot_scatter(df, x_col, y_col, color, size):
    fig = px.scatter(df, x=x_col, y=y_col,
                 color=color, size=size)
    st.plotly_chart(fig)


def user_engagement():
    with open('dashboard/style/style.css') as f:
      css = f.read()

    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


    st.title("User Engagement Analysis")
    st.header('Here is sample data from the cleaned table')
    clean_data_df = load_data()
    st.dataframe(clean_data_df.head(1000))
    app_clean_data_df = clean_data_df[['msisdn_number', 'social_media_total_bytes', 'google_total_bytes',
                                   'email_total_bytes', 'youtube_total_bytes', 'netflix_total_bytes',
                                   'gaming_total_bytes', 'other_total_bytes']]
    app_clean_data_df = app_clean_data_df.groupby(
        'msisdn_number').agg({
            'social_media_total_bytes': 'sum',
            'google_total_bytes': 'sum',
            'email_total_bytes': 'sum',
            'youtube_total_bytes': 'sum',
            'netflix_total_bytes': 'sum',
            'gaming_total_bytes': 'sum',
            'other_total_bytes': 'sum',
        })

    clean_data_df = clean_data_df[['msisdn_number', 'bearer_id', 'dur_ms', 'total_data_bytes']]
    
    clean_data_df = clean_data_df.groupby(
        'msisdn_number').agg({
            'bearer_id': 'count', 
            'dur_ms': 'sum', 
            'total_data_bytes': 'sum'
        })
    clean_data_df = clean_data_df.rename(
        columns={'bearer_id': 'number of xDR Sessions'})

    st.write("")
    st.header('Top 10 Numbers (Users) with highest')
    option = st.selectbox(
        'Top 10 Numbers (Users) with highest',
        ('Number of xDR Sessions', 'Number of Duration', 'Total Data Volume'))

    if option == 'Number of xDR Sessions':
        data = clean_data_df.sort_values(
            'number of xDR Sessions', ascending=False).head(10)
        name = 'number of xDR Sessions'
    elif option == 'Number of Duration':
        data = clean_data_df.sort_values('dur_ms', ascending=False).head(10)
        name = 'dur_ms'
    elif option == 'Total Data Volume':
        data = clean_data_df.sort_values(
            'total_data_bytes', ascending=False).head(10)
        name = 'total_data_bytes'
    data = data.reset_index('msisdn_number')
    fig = px.pie(data, names='msisdn_number', values=name)
    st.plotly_chart(fig)

    # st.write('You selected:', option)

    st.dataframe(data)

    st.write("")
    st.header('Top 10 Engaged Users Per App')
    app_option = st.selectbox(
        'Top 10 Engaged Users Per App',
        ('Social Media', 'Youtube','Google', 'Email', 'Netflix', 'Gaming', 'Other')
    )

    if app_option == 'Social Media':
        app_data = app_clean_data_df.sort_values(
            'social_media_total_bytes',ascending=False
        ).head(10)
        app_name = 'social_media_total_bytes'
    elif app_option == 'Youtube':
        app_data = app_clean_data_df.sort_values(
            'youtube_total_bytes',ascending=False
        ).head(10)
        app_name = 'youtube_total_bytes'
    elif app_option == 'Google':
        app_data = app_clean_data_df.sort_values(
            'google_total_bytes',ascending=False
        ).head(10)
        app_name = 'google_total_bytes'
    elif app_option == 'Email':
        app_data = app_clean_data_df.sort_values(
            'email_total_bytes',ascending=False
        ).head(10)
        app_name = 'email_total_bytes'
    elif app_option == 'Netflix':
        app_data = app_clean_data_df.sort_values(
            'netflix_total_bytes',ascending=False
        ).head(10)
        app_name = 'netflix_total_bytes'
    elif app_option == 'Gaming':
        app_data = app_clean_data_df.sort_values(
            'gaming_total_bytes',ascending=False
        ).head(10)
        app_name = 'gaming_total_bytes'
    else:
        app_data = app_clean_data_df.sort_values(
            'other_total_bytes',ascending=False
        ).head(10)
        app_name = 'other_total_bytes'
    
    app_data = app_data.reset_index('msisdn_number')
    app_fig = px.pie(app_data, names='msisdn_number', values=app_name)
    st.plotly_chart(app_fig)
    st.dataframe(app_data)

    st.title("User Clusters")
    st.write("")
    eng_data_df = load_eng_data()
    st.dataframe(eng_data_df.head(1000))
    st.write("")
    st.markdown("***Users classified into 4 clusters based on their engagement(i.e. number of xDR sessions, duration and total data used).***")
    plotly_plot_scatter(eng_data_df, 'total_data_bytes', 'dur_ms',
            'cluster', 'xdr_sessions')



user_engagement()

util.show_code(user_engagement)
