# pylint: disable=missing-module-docstring
import io

import duckdb
import pandas as pd

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ---------------------------------------------------------------------------------
# EXERCISES LIST
# ---------------------------------------------------------------------------------

data = {
    "theme": ["cross_joins", "cross_joins"],
    "exercise_name": ["beverages_and_food", "sizes_and_trademarks"],
    "tables": [["beverages", "food_items"], ["sizes", "trademarks"]],
    "last_reviewed": ["1970-01-01", "1970-01-02"],
    "solution": ["cross_join_0.sql", "cross_join_1.sql"],
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")

# ---------------------------------------------------------------------------------
# CROSS JOIN EXERCISES
# ---------------------------------------------------------------------------------

# DATABASE 1 : Beverages and food
CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages_df = pd.read_csv(io.StringIO(CSV))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages_df")

CSV2 = """
food_item,food_price
cookie,2.5
chocolatine,2
muffin,3
"""
food_items_df = pd.read_csv(io.StringIO(CSV2))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items_df")

# Database 2 : Sizes and trademarks
SIZES = """
size
XS
M
L
XL
"""
sizes_df = pd.read_csv(io.StringIO(SIZES))
con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes_df")

TRADEMARKS = """
trademark
Nike
Asphalte
Abercrombie
Lewis
"""
trademarks_df = pd.read_csv(io.StringIO(TRADEMARKS))
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks_df")

con.close()
