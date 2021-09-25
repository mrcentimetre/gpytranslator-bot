"""
Based on the codes written by Simon Willison, licensed under Apache 2.0
https://github.com/simonw/db-to-sqlite
"""

from sqlalchemy import create_engine, inspect
from sqlite_utils import Database
import toposort


def db_to_sqlite_func(connection, path):
    if connection.startswith("postgres://"):
        connection = connection.replace("postgres://", "postgresql://")
    db = Database(path)
    db_conn = create_engine(connection).connect()
    inspector = inspect(db_conn)
    tables = toposort.toposort_flatten(
        {
            table: {fk["referred_table"] for fk in inspector.get_foreign_keys(table)}
            for table in inspector.get_table_names()
        }
    )
    for table in tables:
        pks = inspector.get_pk_constraint(table)["constrained_columns"]
        if len(pks) > 1:
            raise Exception("Multiple primary keys not currently supported")
        pk = None
        if pks:
            pk = pks[0]
        fks = inspector.get_foreign_keys(table)
        foreign_keys = [
            (
                # column, type, other_table, other_column
                fk["constrained_columns"][0],
                "INTEGER",
                fk["referred_table"],
                fk["referred_columns"][0],
            )
            for fk in fks
        ]
        results = db_conn.execute("SELECT * FROM {}".format(table))
        rows = (dict(r) for r in results)
        db[table].upsert_all(rows, pk=pk, foreign_keys=foreign_keys)
