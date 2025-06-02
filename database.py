
import sqlite3
def init_db():
    conn = sqlite3.connect('wydatki.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wydatki (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kategoria TEXT NOT NULL,
        kwota REAL NOT NULL,
        data TEXT,
        uwagi TEXT
    )
    """)
    conn.commit()
    return conn

# Funkcja dodawania wydatków
def dodaj_wydatek(conn, kategoria, kwota, data, uwagi):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO wydatki (kategoria, kwota, data, uwagi) VALUES (?, ?, ?, ?)",
                   (kategoria, kwota, data, uwagi))
    conn.commit()

# Funkcja do pobierania wszystkich wydatków
def pobierz_wszystkie_wydatki(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT kategoria, kwota, data, uwagi FROM wydatki")
    return cursor.fetchall()
