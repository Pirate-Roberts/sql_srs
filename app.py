# pylint: disable=missing-module-docstring
import duckdb
import streamlit as st

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# Menu déroulant dans la sidebar
with st.sidebar:
    theme = st.selectbox(
        "How would you like to be contacted ?",
        ("cross_joins", "Joins", "GroupBy", "window_functions"),
        index=None,
        placeholder="Select theme...",
    )

    st.write("You selected:", theme)

    exercise_df = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise_df)
    st.dataframe(exercise_df)

ANSWER = """
SELECT *
FROM beverages
CROSS JOIN food_items
"""

# solution_df = duckdb.sql(ANSWER).df()

st.header("Entrez votre requète SQL:")
query = st.text_area(label="Votre code SQL ici", key="user_input")

#if query:
#    result = duckdb.sql(query).df()
#    st.dataframe(result)
#
#    if len(result.columns) != len(solution_df.columns):
#        st.write("Some columns are missing")
#
#    try:
#        # On utilise le même agencement de colonnes
#        result = result[solution_df.columns]
#    except KeyError as e:
#        st.write("Some columns are missing")
#
#    nb_lines_difference = result.shape[0] - solution_df.shape[0]
#
#    if nb_lines_difference != 0:
#        st.write(
#            f"Result has a {nb_lines_difference} lines difference with the solution"
#        )
#    try:
#        st.dataframe(result.compare(solution_df))
#    except KeyError as e:
#        print()
#
#tab1, tab2 = st.tabs(["Tables", "Solution"])
#
#with tab1:
#    st.write("table : beverages")
#    st.dataframe(beverages)
#    st.write("table : food_items")
#    st.dataframe(food_items)
#    st.write("table : expected")
#    st.dataframe(solution_df)
#
#with tab2:
#    st.write(ANSWER)
#
#
#def my_func():
#    """
#    Docstring
#    :return:
#    """
#    print("prout")
