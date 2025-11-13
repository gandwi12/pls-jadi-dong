import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"

def ensure_db():
    with sqlite3.connect(str(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON;")

        c.execute('''
        CREATE TABLE IF NOT EXISTS restoran (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            created_at TEXT,
            updated_at TEXT
        )
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            description TEXT,
            image_url TEXT,
            restoran_id INTEGER,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY(restoran_id) REFERENCES restoran(id) ON DELETE SET NULL
        )
        ''')

        now = datetime.utcnow().isoformat()

        c.execute('SELECT COUNT(*) FROM restoran')
        if c.fetchone()[0] == 0:
            restos = [
                ('Warung Asri', 'Jl. Merdeka 123', '081234567890', now, now),
                ('Restoran Tiga Rasa', 'Jl. Sudirman 456', '081298765432', now, now),
            ]
            c.executemany(
                'INSERT INTO restoran (name, address, phone, created_at, updated_at) VALUES (?,?,?,?,?)',
                restos
            )

        c.execute('SELECT COUNT(*) FROM menu')
        if c.fetchone()[0] == 0:
            items = [
                ('Nasi Goreng', 25000, 'Nasi goreng spesial', '/static/img/nasi-goreng.jpg', 1, now, now),
                ('Soto Ayam', 18000, 'Soto ayam tradisional', '/static/img/soto-ayam.jpg', 1, now, now),
                ('Gado-gado', 15000, 'Gado-gado saus kacang', '/static/img/gado-gado.jpg', 2, now, now),
            ]
            c.executemany(
                'INSERT INTO menu (name, price, description, image_url, restoran_id, created_at, updated_at) VALUES (?,?,?,?,?,?,?)',
                items
            )

        conn.commit()

if __name__ == "__main__":
    ensure_db()
    print(f"✅ Database created/updated at: {DB_PATH}")