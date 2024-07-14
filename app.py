# pylint: disable=missing-module-docstring
# pylint: disable=unspecified-encoding
# pylint: disable=unused-import
# pylint: disable=exec-used
import logging
import os

import duckdb
import streamlit as st

if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("Creating folder data/")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    with open("init_db.py", "r") as init_db:
        exec(init_db.read())

# Connection à la database
con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# Menu déroulant dans la sidebar
with st.sidebar:
    theme_list = (
        con.execute("SELECT DISTINCT theme FROM memory_state")
        .df()["theme"]
        .unique()
    )
    theme = st.selectbox(
        "How would you like to be contacted ?",
        theme_list,
        index=None,
        placeholder="Select theme...",
    )

    if theme:
        st.write(f"You selected: {theme}")
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}' ORDER BY last_reviewed"
    else:
        select_exercise_query = "SELECT * FROM memory_state ORDER BY last_reviewed"

    exercise_df = con.execute(select_exercise_query).df()
    st.write(exercise_df)

    solution_file = exercise_df.loc[0, "solution"]
    with open(os.path.join("solutions", solution_file), "r") as f:
        solution_query = f.read()
    solution_df = con.execute(solution_query).df()

st.header("Entrez votre requète SQL:")
query = st.text_area(label="Votre code SQL ici", key="user_input")

if query:
    result = con.execute(query).df()
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
        print(f"Erreur : {e}")
    except ValueError as e:
        print(f"Erreur : {e}")

tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:
    exercise_tables = exercise_df.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"table : {table}")
        table_df = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(table_df)

    st.write("table : Solution")
    st.dataframe(solution_df)

with tab2:
    st.write(solution_query)

con.close()
