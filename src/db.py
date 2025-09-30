import os

import sqlite3

from models import Book, User


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data.db')


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            cover TEXT NOT NULL,
            owner_id INTEGER NOT NULL,
            FOREIGN KEY(owner_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()


def create_user(username: str, password: str) -> User:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    user_id = cur.lastrowid
    conn.commit()
    conn.close()
    return User(user_id=user_id, username=username, password=password)


def get_user_by_user_id(user_id: int) -> User:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = ?', (user_id, ))
    user_id, username, password = cur.fetchone()
    conn.close()
    return User(user_id=user_id, username=username, password=password)


def get_user_by_username(username: str) -> tuple[User, int]:
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    except sqlite3.OperationalError:
        conn.close()
        return User(user_id=-1, username='', password=''), 500

    result = cur.fetchone()

    if not result:
        conn.close()
        return User(user_id=-1, username='', password=''), 200

    user_id, username, password = result
    conn.close()
    return User(user_id=user_id, username=username, password=password), 0


def create_book(title: str, author: str, cover: str, owner_id: int) -> Book:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO books (title, author, cover, owner_id) VALUES (?, ?, ?, ?)', (title, author, cover, owner_id))
    book_id = cur.lastrowid
    conn.commit()
    conn.close()
    return Book(book_id=book_id, title=title, author=author, cover=cover, owner_id=owner_id)


def get_book_by_id(book_id: int) -> Book:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books WHERE id = ?', (book_id, ))
    book_id, title, author, cover, owner_id = cur.fetchone()
    conn.close()
    return Book(book_id=book_id, title=title, author=author, cover=cover, owner_id=owner_id)


def get_books_by_owner(owner_id: int) -> list[Book]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books WHERE owner_id = ?', (owner_id,))
    books = cur.fetchall()
    conn.close()
    return [Book(book_id=book_id, title=title, author=author, cover=cover, owner_id=owner_id) for book_id, title, author, cover, owner_id in books]


def delete_book_by_id(book_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM books WHERE id = ?', (book_id, ))
    conn.commit()
    conn.close()


def search_books(query: str, owner_id: int) -> tuple[list[Book], int]:
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM books WHERE title LIKE '%{query}%' OR author LIKE '%{query}%' AND owner_id = {owner_id}")
    except sqlite3.OperationalError:
        conn.close()
        return [], 500

    if (books := cur.fetchall()):
        conn.close()
        return [Book(book_id=book_id, title=title, author=author, cover=cover, owner_id=owner_id) for book_id, title, author, cover, owner_id in books], 0

    conn.close()
    return [], 0
