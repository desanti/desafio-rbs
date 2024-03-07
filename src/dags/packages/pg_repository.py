import json

import pandas as pd
from psycopg2.extras import DictCursor

from hooks.postgres.postgres import PostgresHookExtension


class BaseRepository:
    def __init__(self, conn_id: str, table_name: str, schema_name: str = None, read_bach_size: int = 10000,
                 insert_batch_size: int = 10000):
        self._conn_id = conn_id
        self.table_name = table_name
        self.schema_name = schema_name or "public"
        self.read_batch_size = read_bach_size
        self.insert_batch_size = insert_batch_size

        self._sqlalchemy_conn = None

    def truncate_table(self):
        hook = self._get_hook()
        hook.run(self._format_truncate_query())

    def save(self, df: pd.DataFrame):
        df.to_sql(
            name=self.table_name,
            schema=self.schema_name,
            if_exists="append",
            con=self._get_sqlalchemy_conn(),
            chunksize=self.insert_batch_size,
            index=False,
            method="multi",
        )

    def _get_hook(self) -> PostgresHookExtension:
        return PostgresHookExtension(self._conn_id)

    def _get_sqlalchemy_conn(self):
        if not self._sqlalchemy_conn:
            self._sqlalchemy_conn = self._get_hook().get_sqlalchemy_engine().connect()

        return self._sqlalchemy_conn

    def _get_iter_result(
            self, sql_template, cursor_name="read", params=None
    ):
        with self._get_hook().get_conn() as conn, conn.cursor(
                name=cursor_name, cursor_factory=DictCursor
        ) as cursor:
            cursor.execute(sql_template, params)
            while True:
                results = cursor.fetchmany(self.read_batch_size)
                if not results:
                    break

                yield from results

    def _format_truncate_query(self):
        return f"TRUNCATE TABLE {self.schema_name}.{self.table_name}"


class BaseDatalakeRepository(BaseRepository):
    def __init__(self, table_name: str, schema_name: str):
        super().__init__(conn_id="db_desafio_rbs", table_name=table_name, schema_name=schema_name)


class UserRawRepository(BaseDatalakeRepository):
    def __init__(self):
        super().__init__(table_name="user", schema_name="raw")
        self.read_batch_size = 1

    def save_users(self, users: dict):
        with self._get_hook().get_conn() as conn, conn.cursor() as cursor:
            sql_template = self._get_insert_query()

            cursor.execute(sql_template, {"user": json.dumps(users)})

            conn.commit()

    def get_users(self):
        return self._get_iter_result(self._get_user_events_query())

    @staticmethod
    def _get_user_events_query() -> str:
        return """
             SELECT event
             FROM raw.user
         """

    @staticmethod
    def _get_insert_query():
        return """
            INSERT INTO raw."user" ("event")
            VALUES(%(user)s);
        """


class UserCuratedRepository(BaseDatalakeRepository):
    def __init__(self):
        super().__init__(table_name="user", schema_name="curated")

    def get_all_users(self) -> pd.DataFrame:
        hook = self._get_hook()

        with self._get_hook().get_conn() as conn:
            for df in hook.get_pandas_df_with_conn(self._get_all_users_query(), con=conn, chunksize=1000):
                yield df

    @staticmethod
    def _get_all_users_query():
        return """
            SELECT gender, 
                firstname || ' ' || lastname as name, 
                country, 
                date_of_birth :: DATE as date_of_birth 
            FROM curated."user"        
        """


class BaseApplicationRepository(BaseRepository):
    def __init__(self, table_name: str, schema_name: str = None):
        super().__init__(conn_id="dw_desafio_rbs", table_name=table_name, schema_name=schema_name)


class UserApplicationRepository(BaseApplicationRepository):
    def __init__(self):
        super().__init__(table_name="fact_user")
