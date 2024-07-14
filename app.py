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


def check_users_solution(user_query: str) -> None:
    """
    Check that user SQL query is correct by :
    1 : Checking the columns
    2 : Checking the values
    :param user_query: a string containing the query inserted by the user
    """
    result = con.execute(user_query).df()
    st.dataframe(result)
    if len(result.columns) != len(solution_df.columns):
        st.write("Some columns are missing")
    try:
        # On utilise le même agencement de colonnes
        result = result[solution_df.columns]
    except KeyError:
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


def get_exercises(exercise_theme):
    """
    Get exercises from the chosen theme
    :param exercise_theme : string containing the chose theme for the exercises
    :return df: a dataframe containing all the exercises associated to the chosen theme
    """
    if exercise_theme:
        st.write(f"You selected: {exercise_theme}")
        select_exercise_query = (
            f"SELECT * FROM memory_state WHERE theme = '{exercise_theme}' "
            "ORDER BY last_reviewed"
        )
    else:
        select_exercise_query = "SELECT * FROM memory_state ORDER BY last_reviewed"
    df = con.execute(select_exercise_query).df()
    st.write(df)

    return df


# Menu déroulant dans la sidebar
with st.sidebar:
    theme_list = (
        con.execute("SELECT DISTINCT theme FROM memory_state").df()["theme"].unique()
    )
    theme = st.selectbox(
        "How would you like to be contacted ?",
        theme_list,
        index=None,
        placeholder="Select theme...",
    )

    exercise_df = get_exercises(theme)

    solution_file = exercise_df.loc[0, "solution"]
    with open(os.path.join("solutions", solution_file), "r") as f:
        solution_query = f.read()
    solution_df = con.execute(solution_query).df()

st.header("Entrez votre requète SQL:")
query = st.text_area(label="Votre code SQL ici", key="user_input")

if query:
    check_users_solution(query)

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
