import sqlalchemy as sa
import pandas as pd


def get_alchemy_engine_dwh():
    ch_host = ''
    ch_port = ''
    ch_db = ''
    ch_user = ''
    ch_pass = ''
    engine = sa.create_engine(f'clickhouse+native://{ch_user}:{ch_pass}@{ch_host}:{ch_port}/{ch_db}')

    return engine


def get_pandas_df(sql):

    engine = get_alchemy_engine_dwh()

    df = pd.read_sql(
        sql=sql,
        con=engine
    )

    return df

