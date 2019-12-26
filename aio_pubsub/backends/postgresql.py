import uuid
from time import time

from aio_pubsub.interfaces import Subscriber, PubSub
from aio_pubsub.typings import Message

aiopg_not_installed = False
try:
    from aiopg import Pool
    from psycopg2.extras import Json

    aiopg_not_installed = True
except ImportError:
    pass  # pragma: no cover

ADD_TABLE_SQL = """
create table if not exists {table_name}
(
    msg_id uuid,
    created_at int,
    channel varchar(256),
    data jsonb
);
create unique index if not exists {table_name}_msg_id_uindex
    on {table_name} (msg_id);
"""

SELECT_MSG = """
select msg_id, created_at, channel, data from {table_name}
 where channel=%(channel)s order by created_at limit 1 for update skip locked;
"""

REMOVE_MSG = """
delete from {table_name} where msg_id=%(msg_id)s;
"""

INSERT_MSG_SQL = """
insert into {table_name} (msg_id, created_at, channel, data)
 VALUES (%(msg_id)s, %(created_at)s, %(channel)s, %(data)s);
"""


class PostgreSQLSubscriber(Subscriber):
    def __init__(self, conn_pool, table_name, channel):
        self.channel = channel
        self.conn_pool = conn_pool
        self.table_name = table_name

    def __aiter__(self):
        return self

    async def __anext__(self):
        select_sql = SELECT_MSG.format(table_name=self.table_name)
        remove_sql = REMOVE_MSG.format(table_name=self.table_name)
        async with self.conn_pool.acquire() as pool:
            async with pool.cursor() as cursor:
                while True:
                    async with cursor.begin():
                        await cursor.execute(select_sql, {"channel": self.channel})
                        res = await cursor.fetchone()
                        if res:
                            msg_id, _, _, data = res
                            try:
                                return data
                            finally:
                                await cursor.execute(remove_sql, {"msg_id": msg_id})


class PostgreSQLPubSub(PubSub):
    def __init__(self, conn_pool: Pool, table_name="aio_pubsub"):
        if aiopg_not_installed is False:
            raise RuntimeError("Please install `aiopg`")  # pragma: no cover
        self.conn_pool = conn_pool
        self.table_name = table_name

    async def init(self):
        create_table_sql = ADD_TABLE_SQL.format(table_name=self.table_name)
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(create_table_sql)

    async def publish(self, channel: str, message: Message):
        insert_sql = INSERT_MSG_SQL.format(table_name=self.table_name)
        async with self.conn_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                params = {
                    "msg_id": uuid.uuid4(),
                    "created_at": int(time()),
                    "channel": channel,
                    "data": Json(message),
                }
                await cursor.execute(insert_sql, params)

    async def subscribe(self, channel):
        return PostgreSQLSubscriber(self.conn_pool, self.table_name, channel)
