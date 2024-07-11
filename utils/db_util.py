from peewee import SqliteDatabase
import os
import sys

base_dir = os.path.dirname(sys.executable)

if not os.path.exists(f"{base_dir}/db_data"):
    print(f"=====pwd::::{base_dir}=================")
    os.mkdir(f"{base_dir}/db_data")

ds_db = SqliteDatabase(
    f'{base_dir}/db_data/daba.db',
    pragmas={
        'journal_mode': 'wal',  # WAL-mode.
        'cache_size': -64 * 1024,  # 64MB cache.
    },
)
ds_db.connect()



