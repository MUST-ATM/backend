import aiosqlite

DATABASE = "database.db"

async def create_tables():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE,
            name TEXT
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS balance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            foreign_account REAL,
            hkd_account REAL,
            mop_account REAL,
            FOREIGN KEY (user_id) REFERENCES user (user_id)
        )
        """)
        await db.commit()
        
async def insert_initial_data():
    async with aiosqlite.connect(DATABASE) as db:
        # 插入初始用户数据
        await db.execute("INSERT OR IGNORE INTO user (user_id, name) VALUES (?, ?)", ("00001", "Alice"))
        await db.execute("INSERT OR IGNORE INTO user (user_id, name) VALUES (?, ?)", ("00002", "Bob"))
        # 插入初始账户余额数据
        await db.execute("INSERT OR IGNORE INTO balance (user_id, foreign_account, hkd_account, mop_account) VALUES (?, ?, ?, ?)", ("00001", 1000.0, 3000.0, 2000.0))
        await db.execute("INSERT OR IGNORE INTO balance (user_id, foreign_account, hkd_account, mop_account) VALUES (?, ?, ?, ?)", ("00002", 1500.0, 2500.0, 3500.0))
        await db.commit()

async def get_connection():
    return await aiosqlite.connect(DATABASE)
