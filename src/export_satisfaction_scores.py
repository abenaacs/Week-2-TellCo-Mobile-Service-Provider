from sqlalchemy import create_engine
import pandas as pd


def export_to_database(df, table_name, db_url):
    engine = create_engine(db_url)
    with engine.connect() as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Exported {table_name} to database.")
