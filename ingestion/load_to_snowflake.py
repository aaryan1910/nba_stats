import os
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector
from dotenv import load_dotenv
from fetch_player_stats import fetch_player_stats
from fetch_advanced_stats import fetch_advanced_stats
from fetch_player_salaries import fetch_player_salaries

load_dotenv(dotenv_path="../.env")

def get_snowflake_connection():
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE")
    )

def load_dataframe(conn, df, table_name):
    print(f"Loading {len(df)} rows into {table_name}...")
    df.columns = [col.upper() for col in df.columns]
    success, nchunks, nrows, _ = write_pandas(conn, df, table_name, auto_create_table=True)
    print(f"Successfully loaded {nrows} rows into {table_name}")

def main():
    print("Starting Snowflake load...")
    conn = get_snowflake_connection()

    # Fetch all three datasets
    player_stats = fetch_player_stats()
    advanced_stats = fetch_advanced_stats()
    player_salaries = fetch_player_salaries()

    # Load to Snowflake RAW schema
    load_dataframe(conn, player_stats, "RAW_PLAYER_STATS")
    load_dataframe(conn, advanced_stats, "RAW_ADVANCED_STATS")
    load_dataframe(conn, player_salaries, "RAW_PLAYER_SALARIES")

    conn.close()
    print("All data loaded successfully!")

if __name__ == "__main__":
    main()