# Loads pandas DataFrames from ingestion scripts into Snowflake RAW tables and overwrites the target table on each load. 

import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import os

def get_connection():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        role="TRANSFORM_ROLE",
        warehouse="F1_WH",
        database="F1_DB",
        schema="RAW"
    )


def load_df(df, table_name: str, overwrite: bool = True):
    if df.empty:
        print(f"Skipping {table_name} — empty dataframe")
        return
    conn = get_connection()
    df.columns = [c.upper() for c in df.columns]
    success, nchunks, nrows, _ = write_pandas(
        conn, df, table_name.upper(), overwrite=overwrite
    )
    print(f"Loaded {nrows} rows into {table_name} (overwrite={overwrite})")
    conn.close()