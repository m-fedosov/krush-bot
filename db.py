import sqlite3
from config import DB_PATH


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # доступ к колонкам по имени
    return conn


def init_db():
    """Создаёт таблицу users если не существует."""
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id         INTEGER UNIQUE NOT NULL,
                username      TEXT,
                first_name    TEXT,
                status        TEXT NOT NULL DEFAULT 'REGISTERED',
                registered_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.commit()


def get_user(tg_id: int) -> sqlite3.Row | None:
    """Возвращает пользователя по tg_id или None."""
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE tg_id = ?", (tg_id,)
        ).fetchone()


def register_user(tg_id: int, username: str | None, first_name: str) -> bool:
    """
    Регистрирует пользователя.
    Возвращает True если создан новый, False если уже существовал.
    """
    with get_conn() as conn:
        cursor = conn.execute("""
            INSERT OR IGNORE INTO users (tg_id, username, first_name, status)
            VALUES (?, ?, ?, 'REGISTERED')
        """, (tg_id, username, first_name))
        conn.commit()
    return cursor.rowcount > 0  # True = новый, False = уже был