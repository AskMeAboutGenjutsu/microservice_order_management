import aiosqlite

DB_KEY = 'database'


async def create_database_connection(app, db_name):
    """
    Подключение к бд SQLite
    """
    db = await aiosqlite.connect(db_name)
    app[DB_KEY] = db


async def destroy_database_connection(app):
    """
    Отключение от бд SQLite
    """
    db = app[DB_KEY]
    await db.close()