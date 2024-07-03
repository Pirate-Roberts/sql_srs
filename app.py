import streamlit as st
import pandas as pd
import duckdb

st.write("Hello world!")

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data=data)

tab1, tab2, tab3 = st.tabs(['Cat', 'Dog', 'Owl'])

with tab1:
    st.header("A cat!")
    sql_query = st.text_area(label="Entrez votre input.")
    df_sql = duckdb.sql(sql_query).df()
    st.write(f"Vous avez entré la query suivante: {sql_query}")
    st.write(df)
    st.write(df_sql)
