from peewee import SqliteDatabase
import os


if not os.path.exists(f"{os.getcwd()}/db_data"):
    print(f"=====pwd::::{os.getcwd()}=================")
    os.mkdir(f"{os.getcwd()}/db_data")

ds_db = SqliteDatabase(
    './db_data/daba.db',
    pragmas={
        'journal_mode': 'wal',  # WAL-mode.
        'cache_size': -64 * 1024,  # 64MB cache.
    },
)
ds_db.connect()



