from airflow.providers.postgres.hooks.postgres import PostgresHook
from pandas.io import sql as psql


class PostgresHookExtension(PostgresHook):
    def get_pandas_df_with_conn(self, sql, con, parameters=None, **kwargs):
        return psql.read_sql(sql, con=con, params=parameters, **kwargs)
