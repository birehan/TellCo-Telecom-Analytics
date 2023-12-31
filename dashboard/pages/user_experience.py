
import plotly.express as px
import pandas as pd
import streamlit as st
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(script_dir, "../")

sys.path.insert(0, parent_dir)

import utils as util

@st.cache_data()
def load_data():
    clean_data_df = pd.read_csv("data/cleaned_tellco_data.csv")
    return clean_data_df

@st.cache_data()
def load_eng_data():
    eng_data_df = pd.read_csv("data/tellco_user_experience_data.csv")
    return eng_data_df

clean_data_df = load_data()
eng_data_df = load_eng_data()


def user_experience():
    with open('dashboard/style/style.css') as f:
      css = f.read()

    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


    st.title("User Experience Analysis")
    tellco_exprience_df = load_data()
  
    tellco_exprience_df = tellco_exprience_df[[
        'msisdn_number', 'total_avg_rtt_dl_ms', 'total_avg_bearer_tp_kbps', 'total_tcp_dl_retrans_vol_bytes', 'handset_type']]
    tellco_exprience_df1 = tellco_exprience_df.groupby(
        'msisdn_number').agg({'total_avg_rtt_dl_ms': 'sum', 'total_avg_bearer_tp_kbps': 'sum', 'total_tcp_dl_retrans_vol_bytes': 'sum', 'handset_type': [lambda x: x.mode()[0]]})  # ' '.join(x)
    tellco_exprience_df = pd.DataFrame(columns=[
        "total_avg_rtt_dl_ms",
        "total_avg_bearer_tp_kbps",
        "total_tcp_dl_retrans_vol_bytes",
        "handset_type"])

    tellco_exprience_df["total_avg_rtt_dl_ms"] = tellco_exprience_df1["total_avg_rtt_dl_ms"]['sum']
    tellco_exprience_df["total_avg_bearer_tp_kbps"] = tellco_exprience_df1["total_avg_bearer_tp_kbps"]['sum']
    tellco_exprience_df["total_tcp_dl_retrans_vol_bytes"] = tellco_exprience_df1[
        "total_tcp_dl_retrans_vol_bytes"]['sum']
    tellco_exprience_df["handset_type"] = tellco_exprience_df1["handset_type"]['<lambda>']
    option = st.selectbox(
        'Top 10 of the top, bottom and most frequent Datas Based on',
        ('total_avg_rtt_dl_ms', 'total_avg_bearer_tp_kbps', 'total_tcp_dl_retrans_vol_bytes'))

    data = tellco_exprience_df.sort_values(option, ascending=False)
    highest = data.head(10)[option]
    lowest = data.tail(10)[option]
    most = tellco_exprience_df[option].value_counts().head(10)
    
    st.header("Highest")
    highest = highest.reset_index('msisdn_number')
    fig = px.bar(highest, x='msisdn_number', y=option)
    fig.update_layout(xaxis_type='category')
    st.plotly_chart(fig)
    
    st.header("Lowest")
    lowest = lowest.reset_index('msisdn_number')
    fig = px.bar(lowest, x='msisdn_number', y=option)
    fig.update_layout(xaxis_type='category')
    st.plotly_chart(fig)
    
    st.header("Most")
    st.dataframe(most)

    exp_data_df = load_eng_data()
    st.title("User Clusters")
    st.write("")
    st.dataframe(exp_data_df.head(1000))
    st.write("")
    st.write("")
    st.markdown("***Users classified into 3 clusters based on their experience(i.e. average RTT, TCP retransmission', and throughput).***")
    util.plotly_plot_scatter(exp_data_df, 'total_tcp_dl_retrans_vol_bytes', 'total_avg_bearer_tp_kbps',
            'cluster', 'total_avg_rtt_dl_ms')
    


st.sidebar.header("User Experience")


user_experience()

util.show_code(user_experience)
