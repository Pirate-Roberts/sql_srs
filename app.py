# pylint: disable=missing-module-docstring
import io

import duckdb
import pandas as pd
import streamlit as st

CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item,food_price
cookie,2.5
chocolatine,2
muffin,3
"""

food_items = pd.read_csv(io.StringIO(CSV2))

# Menu déroulant dans la sidebar
with st.sidebar:
    option = st.selectbox(
        "How would you like to be contacted ?",
        ("Joins", "GroupBy", "Windows Functions", ""),
        index=None,
        placeholder="Select theme...",
    )

    st.write("You selected:", option)

ANSWER = """
SELECT *
FROM beverages
CROSS JOIN food_items
"""

solution_df = duckdb.sql(ANSWER).df()

st.header("Entrez votre requète SQL:")
query = st.text_area(label="Votre code SQL ici", key="user_input")

if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

    if len(result.columns) != len(solution_df.columns):
        st.write("Some columns are missing")

    try:
        # On utilise le même agencement de colonnes
        result = result[solution_df.columns]
    except KeyError as e:
        st.write("Some columns are missing")

    nb_lines_difference = result.shape[0] - solution_df.shape[0]

    if nb_lines_difference != 0:
        st.write(
            f"Result has a {nb_lines_difference} lines difference with the solution"
        )
    try:
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        print()

tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:
    st.write("table : beverages")
    st.dataframe(beverages)
    st.write("table : food_items")
    st.dataframe(food_items)
    st.write("table : expected")
    st.dataframe(solution_df)

with tab2:
    st.write(ANSWER)


def my_func():
    """
    Docstring
    :return:
    """
    print("prout")
