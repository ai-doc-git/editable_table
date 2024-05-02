# Import python packages
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import datetime
from annotated_text import annotated_text

# Page Congifuration
st.set_page_config(
    page_title='PROTOTYPE', 
    page_icon='🕐', 
    layout='wide'
)

st.markdown("<h1 style='text-align: center; color: rgb(0, 0, 0);'> PROTOTYPE </h1>", unsafe_allow_html=True)
    
# Data
uploaded_file = st.file_uploader("Upload data:")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file,sep=';')
    # st.dataframe(df)

# df = pd.read_csv('dummy.csv',sep=';')


    col1,col2,col3,col4,col5 = st.columns(5)
    prod = col1.selectbox('Product', df['Product'].unique(), index=None)
    sub_prod = col2.selectbox('Sub-Product', df['Sub-Product'].unique(), index=None)
    reason = col3.selectbox('Reason', df['Reason'].unique(), index=None)
    month = col4.selectbox('Month', df['Month'].unique(), index=None)
    ingestion = col5.selectbox('Ingestion', df['Ingestion'].unique(), index=None)


    df_filter = pd.DataFrame()

    if prod:
        df_filter = df.loc[df['Product'].isin([prod])]
    if sub_prod:
        df_filter = df_filter.loc[df_filter['Sub-Product'].isin([sub_prod])]
    if reason:
        df_filter = df_filter.loc[df_filter['Reason'].isin([reason])]
    if month:
        df_filter = df_filter.loc[df_filter['Month'].isin([month])]
    if ingestion:
        df_filter = df_filter.loc[df_filter['Ingestion'].isin([ingestion])]


    df_container2 = st.dataframe(df_filter, use_container_width=True)


    adj_number = st.number_input('Adjustment Input:')

    if adj_number:

        annotated_text(
        "Selection : ",
        (df_filter['Product'].unique()[0], "Product"), "          ",
        (df_filter['Sub-Product'].unique()[0], "Sub-Product"), "          ",
        (df_filter['Reason'].unique()[0], "Reason"), "          ",
        (df_filter['Month'].unique()[0], "Month"), "          "
        )

        df_filter['Adjusted Forecast'] = df_filter['Forecast'] + adj_number
        st.write("Adjusted Forecast: ")
        st.dataframe(df_filter[['Ingestion','Forecast','Adjusted Forecast']], use_container_width=True)




    submit = st.button("Freeze Adjustment", type="primary", use_container_width=True)
    if submit:
        df_filter['Adjustment'] = adj_number
        df_filter['Adjustment Date'] = datetime.datetime.now()
        st.dataframe(df_filter[['Product','Sub-Product','Reason','Month','Adjustment','Adjustment Date']].head(1), use_container_width=True)
        st.snow()
