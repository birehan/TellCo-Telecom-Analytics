import pandas as pd
import streamlit as st

import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(script_dir, "../")

sys.path.insert(0, parent_dir)

import utils as util

@st.cache_data()
def load_sat_only_scores_data():
    sat_only_scores_df = pd.read_csv("data/user_satisfaction.csv")
    return sat_only_scores_df

@st.cache_data()
def load_sat_score_data():
    sat_score_df = pd.read_csv("data/tellco_user_satisfaction_score_data.csv")
    return sat_score_df

def user_satisfaction():
    with open('dashboard/style/style.css') as f:
      css = f.read()

    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)



    st.title("User Satisfaction Analysis")
    st.write("")
    st.header("User engagement score table")
    sat_score_df = load_sat_score_data()
    sat_only_scores_df = load_sat_only_scores_data()
    
    st.dataframe(sat_only_scores_df)

    eng_df = sat_score_df[['msisdn_number','xdr_sessions', 'dur_ms', 'total_data_bytes', 'engagement_score']]
    
    sat_score_df_agg = sat_score_df.groupby(
        'msisdn_number').agg({
            'dur_ms': 'sum', 
            'total_data_bytes': 'sum',
           'engagement_score':'sum',
           'engagement_cluster':'sum',
           'total_avg_rtt_dl_ms':'sum',
           'total_avg_bearer_tp_kbps':'sum',
           'total_tcp_dl_retrans_vol_bytes':'sum',
           'experience_score':'sum',
           'experience_cluster':'sum',
           'satisfaction_score':'sum',
        })
    
    sat_only_score_df_agg = sat_only_scores_df.groupby(
        'msisdn_number').agg({
           'engagement_score':'sum',
           'experience_score':'sum',
           'cluster':'sum',
           'satisfaction_score':'sum',
        })

    st.write(eng_df.head(1000))
    st.write("")
    st.markdown("**Users classified into 6 clusters based on their engagement(i.e. number of xdr_sessions, duration and total data used).**")
    util.plotly_plot_scatter(sat_score_df, 'total_data_bytes', 'dur_ms',
            'engagement_cluster', 'xdr_sessions')

    
    st.write("")
    st.header("User experience score table")
    exp_df = sat_score_df[['msisdn_number', 'total_avg_rtt_dl_ms',
        'total_avg_bearer_tp_kbps', 'total_tcp_dl_retrans_vol_bytes', 'experience_score']]
    st.write(exp_df.head(1000))
    st.write("")
    st.markdown("**Users classified into 3 clusters based on their experience(i.e. average RTT, TCP retransmission', and throughput).**")
    util.plotly_plot_scatter(sat_score_df, 'total_tcp_dl_retrans_vol_bytes', 'total_avg_bearer_tp_kbps',
            'experience_cluster', 'total_avg_rtt_dl_ms')

    st.write("")
    st.header("User satisfaction score table")
    sat_df = sat_only_scores_df[['msisdn_number', 'engagement_score', 'experience_score', 'satisfaction_score']]
    st.write(sat_df.head(1000))
    st.write("")
    st.markdown("**Users classified into 2 clusters based on their satisfactio(i.e. engagement score and experience score).**")
    util.plotly_plot_scatter(sat_only_scores_df, 'engagement_score', 'experience_score',
            'cluster', 'satisfaction_score')
    
    st.write("")
    st.header('Top 10 Numbers (Users) with highest')
    option = st.selectbox(
        'Top 10 Numbers (Users) with highest',
        ('Engagement Score', 'Experience Score', 'Satisfaction Score'))

    if option == 'Engagement Score':
        data = sat_score_df_agg.sort_values(
            'engagement_score', ascending=False).head(10)
        sat_only_data = sat_only_score_df_agg.sort_values(
            'engagement_score', ascending=False).head(10)
        name = 'engagement_score'
    elif option == 'Experience Score':
        data = sat_score_df_agg.sort_values(
            'experience_score', ascending=False).head(10)
        sat_only_data = sat_only_score_df_agg.sort_values(
            'experience_score', ascending=False).head(10)
        name = 'experience_score'
    else:
        data = sat_score_df_agg.sort_values(
            'satisfaction_score', ascending=False).head(10)
        sat_only_data = sat_only_score_df_agg.sort_values(
            'satisfaction_score', ascending=False).head(10)
        name = 'satisfaction_score'
    
    data = data.reset_index('msisdn_number')
 

    st.dataframe(sat_only_data)

    st.write("")
    st.dataframe(data)


st.sidebar.header("User Satisfaction")


user_satisfaction()

util.show_code(user_satisfaction)
