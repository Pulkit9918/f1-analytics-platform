import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px

st.set_page_config(page_title="F1 Race Strategy Analytics", layout="wide")

conn = snowflake.connector.connect(
    account=st.secrets["SNOWFLAKE_ACCOUNT"],
    user=st.secrets["SNOWFLAKE_USER"],
    password=st.secrets["SNOWFLAKE_PASSWORD"],
    role="TRANSFORM_ROLE",
    warehouse="F1_WH",
    database="F1_DB",
    schema="ANALYTICS"
)

st.title("🏎️ F1 Race Strategy & Performance Analytics")

tab1, tab2, tab3 = st.tabs(["Championship Progression", "Qualifying vs Race Pace", "Tire Strategy"])

with tab1:
    df = pd.read_sql("SELECT * FROM MART_CHAMPIONSHIP_PROGRESSION", conn)
    fig = px.line(df, x="ROUND", y="CUMULATIVE_POINTS", color="DRIVER_NAME",
                  title="Championship Points Progression")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    df = pd.read_sql("SELECT * FROM MART_QUALIFYING_VS_RACE_PACE", conn)
    fig = px.scatter(df, x="GRID_POSITION", y="FINISH_POSITION", color="DRIVER_NAME",
                      hover_data=["RACE_NAME"], title="Grid Position vs Finish Position")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    df = pd.read_sql("SELECT * FROM MART_TIRE_STINT_PERFORMANCE", conn)
    fig = px.box(df, x="COMPOUND", y="AVG_LAP_TIME_SEC", color="COMPOUND",
                  title="Lap Time Distribution by Tire Compound")
    st.plotly_chart(fig, use_container_width=True)