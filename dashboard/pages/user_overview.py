import pandas as pd
import streamlit as st
import plotly.express as px
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(script_dir, "../")
sys.path.insert(0, parent_dir)

import utils as util

@st.cache_data()
def load_data():
    clean_data_df = pd.read_csv("data/cleaned_tellco_data.csv")
    return clean_data_df

clean_data_df = load_data()

def user_overview() -> None:
    with open('dashboard/style/style.css') as f:
      css = f.read()

    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)



    st.title("User Overview Analysis")
   

    st.header('Here we have an overview of our data set')
    st.write(clean_data_df)
    st.header("Top Handsets")
    st.write(clean_data_df['handset_type'].value_counts())
    fig = px.bar(clean_data_df['handset_type'].value_counts().rename_axis(
        'Handset Type').reset_index(name='counts').head(10), x='Handset Type', y='counts')
    st.plotly_chart(fig)
    
    top_handset_manufacturers = clean_data_df['handset_manufacturer'].value_counts(
    ).head(3)
    top_handset_manufacturers = clean_data_df[clean_data_df["handset_manufacturer"].isin(
        top_handset_manufacturers.index.tolist())]
    top_handsets = top_handset_manufacturers['handset_type'].groupby(
        clean_data_df['handset_manufacturer']).apply(lambda x: x.value_counts().head(5))
    st.header("Top Handsets by manufactureres")
    st.dataframe(top_handsets)
    
    st.header("User with the top number of sessions")
    number_of_xdr = clean_data_df.groupby('msisdn_number')['msisdn_number'].agg(
        'count').reset_index(name='bearer_id').sort_values(by='bearer_id', ascending=False)
    number_of_xdr.rename(
        columns={number_of_xdr.columns[1]: 'number of xDR sessions'}, inplace=True)
    st.dataframe(number_of_xdr.head(10))
    fig = px.bar(number_of_xdr.head(10), x='msisdn_number',
                 y='number of xDR sessions')
    fig.update_layout(xaxis_type='category')
    st.plotly_chart(fig)
    
    st.header("User with the top total duration of sessions")
    sum_duration_of_sessions = clean_data_df.groupby(
        'msisdn_number').agg({'dur_ms': 'sum'}).sort_values(by='dur_ms', ascending=False)
    sum_duration_of_sessions.rename(columns={
                                    sum_duration_of_sessions.columns[0]: 'duration of xDR sessions (total)'}, inplace=True)
    sum_duration_of_sessions['duration of xDR sessions (total)'] = sum_duration_of_sessions['duration of xDR sessions (total)'].astype(
        "int64")
    st.dataframe(sum_duration_of_sessions.head(10))
    
    st.header("User with the top avarage duration of sessions")
    avg_duration_of_sessions = clean_data_df.groupby(
        'msisdn_number').agg({'dur_ms': 'mean'}).sort_values(by='dur_ms', ascending=False)
    avg_duration_of_sessions.rename(columns={
                                    avg_duration_of_sessions.columns[0]: 'duration of xDR sessions (AVG)'}, inplace=True)
    avg_duration_of_sessions
    
    # st.dataframe(avg_duration_of_sessions.head(10))
    st.header("User with the top total data used")
    data_volumes = clean_data_df.groupby('msisdn_number')[['total_ul_bytes', 'total_dl_bytes',
                                                           'total_data_bytes']].sum().sort_values(by='total_data_bytes', ascending=False)
    data_volumes['total_data_bytes'] = data_volumes['total_data_bytes'].astype(
        "int64")
    data_volumes['total_dl_bytes'] = data_volumes['total_dl_bytes'].astype(
        "int64")
    data_volumes['total_ul_bytes'] = data_volumes['total_ul_bytes'].astype(
        "int64")
    st.dataframe(data_volumes)



st.sidebar.header("User Overview")

user_overview()

util.show_code(user_overview)