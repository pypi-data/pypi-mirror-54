from collections import namedtuple
import logging
from typing import Any, Dict, Optional, TYPE_CHECKING

from sqlalchemy.sql import text
from sqltask.classes.common import BaseDataSource, Lookup
if TYPE_CHECKING:
    from sqltask.classes.context import EngineContext


class SqlDataSource(BaseDataSource):
    @classmethod
    def create(cls,
               name: str,
               sql: str,
               params: Optional[Dict[str, Any]],
               engine_context: "EngineContext",
               schema: Optional[str] = None,
               ) -> "SqlDataSource":
        """
        Factory method for creating an instance of the class. The preferred way of
        creating a sql datasource.

        :param name: name of data source
        :param sql: sql query with parameter values prefixed with a colon, e.g.
        `WHERE dt <= :batch_date`
        :param params: mapping between parameter keys and values, e.g.
        `{"batch_date": date(2010, 1, 1)}`
        :param schema: schema to use when executing query. Uses schema defined
        in sql_engine if left undefined.
        :param engine_context: engine used to execute the query.

        :return:
        """
        params = params or {}
        schema = schema or engine_context.schema
        return cls(name, sql, params, engine_context, schema)

    def __init__(self,
                 name: str,
                 sql: str,
                 params: Dict[str, Any],
                 engine_context: "EngineContext",
                 schema: str = None,
                 ):
        super().__init__(name)
        self.sql = sql
        self.params = params or {}
        self.sql_engine = engine_context
        self.schema = schema or engine_context.schema

    def __iter__(self):
        rows = self.sql_engine.engine.execute(text(self.sql), self.params)
        for row in rows:
            yield Lookup(self, dict(zip(row.keys(), row.values())))


class LookupSource(BaseDataSource):
    @classmethod
    def create(cls,
               name: str,
               sql: str,
               params: Optional[Dict[str, Any]],
               engine_context: "EngineContext",
               schema: Optional[str] = None,
               keys: int = 1,
               ) -> "LookupSource":
        """
        Factory method for creating an instance of the class. The preferred way of
        creating a lookup source.

        :param name: name of data source
        :param sql: sql query with parameter values prefixed with a colon, e.g.
        `WHERE dt <= :batch_date`
        :param params: mapping between parameter keys and values, e.g.
        `{"batch_date": date(2010, 1, 1)}`
        :param schema: schema to use when executing query. Uses schema defined
        in sql_engine if left undefined.
        :param keys: number of keys in dict key.
        :param engine_context: engine used to execute the query.

        :return:
        """
        params = params or {}
        schema = schema or engine_context.schema
        return cls(name, sql, params, engine_context, schema, keys)

    def __init__(self,
                 name: str,
                 sql: str,
                 params: Dict[str, Any],
                 engine_context: "EngineContext",
                 schema: Optional[str] = None,
                 keys: int = 1,
                 ):
        super().__init__(name)
        self.sql = sql
        self.params = params or {}
        self.engine_context = engine_context
        self.schema = schema or engine_context.schema
        self.keys = keys

    def get_lookup(self) -> Lookup:
        rows = self.engine_context.engine.execute(text(self.sql), self.params)
        cursor = rows.cursor
        self.KeyTuple = namedtuple(self.name, rows.keys())
        if self.keys < 1:
            raise Exception(f"A minimum of 1 key is needed for a lookup")
        elif len(rows.keys()) <= self.keys:
            raise Exception(
                f"Too few columns in lookup `name`: {len(cursor.description)} found, expected more than {self.keys}")
        else:
            lookup = {}

        row_count, duplicate_count = 0, 0
        for row in rows:
            row_count += 1
            # regular key-value lookup
            if self.keys == 1:
                key = row[0]
            else:
                key = KeyTuple([row.values()])

            if len(rows.keys()) == self.keys + 1:
                value = row[self.keys]
            else:
                value = {rows.keys()[i]: row[i]
                         for i in range(self.keys, len(rows.keys()))}
                value = Lookup(self, value)
            if key in lookup:
                duplicate_count += 1
            else:
                lookup[key] = value

        if duplicate_count > 0:
            logging.warning(
                f"Query result for lookup `{self.name}` has {duplicate_count} duplicate keys, ignoring duplicate rows")
        logging.info(f"Finished populating lookup `{self.name}` with {len(lookup)} rows")

        return Lookup(self, lookup)
