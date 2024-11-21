import sqlite3
import json
import os


BOOKS_FILE = "database/books.json"


def create_library_table():
    """
    Создает таблицу 'library' в базе данных, если она не существует.
    """

    conn = sqlite3.connect("database/library.db")
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS library (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              author TEXT NOT NULL,
              year INTEGER,
              status TEXT CHECK(status IN ('в наличии', 'выдана'))
              );
    """
    )

    conn.commit()
    conn.close()


def add_book(title, author, year):
    """
    Добавляет книгу в библиотеку.

    :param title: Название книги.
    :param author: Автор книги.
    :param year: Год издания книги.
    """

    conn = sqlite3.connect("database/library.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM library WHERE title = ? AND author = ? AND year = ?",
        (title, author, year),
    )

    if c.fetchone() is None:
        c.execute(
            "INSERT INTO library (title, author, year, status) VALUES (?, ?, ?, 'в наличии');",
            (title, author, year),
        )

    conn.commit()
    conn.close()
    save_books_to_json()


def delete_book(book_id):
    """
    Удаляет книгу из библиотеки по ID.

    :param book_id: ID книги, которую нужно удалить.
    :return: True, если книга была удалена, иначе False.
    """

    conn = sqlite3.connect("database/library.db")
    c = conn.cursor()

    c.execute("DELETE FROM library WHERE id = ?", (book_id,))
    deleted_rows = c.rowcount  # Получаем количество удаленных строк

    conn.commit()
    conn.close()
    save_books_to_json()

    return (
        deleted_rows > 0
    )  # Возвращаем True, если была удалена хотя бы одна строка, иначе False


def search_book(title=None, author=None, year=None):
    """
    Ищет книги в библиотеке по заданным параметрам.

    :param title: Название книги (необязательный).
    :param author: Автор книги (необязательный).
    :param year: Год издания книги (необязательный).
    :return: Список найденных книг.
    """

    conn = sqlite3.connect("database/library.db")
    c = conn.cursor()

    query = "SELECT * FROM library WHERE 1=1"
    parameters = []

    if title:
        query += " AND title LIKE ?"
        parameters.append(f"%{title}%")

    if author:
        query += " AND author LIKE ?"
        parameters.append(f"%{author}%")

    if year:
        query += " AND year LIKE ?"
        parameters.append(f"%{year}%")

    c.execute(query, parameters)
    results = c.fetchall()

    conn.close()
    return results


def display_all_books():
    """
    Возвращает список всех книг в библиотеке.

    :return: Список книг с их данными (ID, название, автор, год, статус).
    """

    conn = sqlite3.connect("database/library.db")
    c = conn.cursor()

    c.execute("SELECT id, title, author, year, status FROM library")
    results = c.fetchall()

    conn.close()
    return results


def change_status_book(book_id, new_status):
    """
    Изменяет статус книги по ID.

    :param book_id: ID книги, статус которой нужно изменить.
    :param new_status: Новый статус книги (в наличии/выдана).
    """

    conn = sqlite3.connect("database/library.db")
    c = conn.cursor()

    c.execute("UPDATE library SET status = ? WHERE id = ?", (new_status, book_id))

    conn.commit()
    conn.close()
    save_books_to_json()


def save_books_to_json():
    """
    Сохраняет все книги из библиотеки в JSON-файл.
    """

    books = display_all_books()
    books_list = [
        {
            "id": book[0],
            "title": book[1],
            "author": book[2],
            "year": book[3],
            "status": book[4],
        }
        for book in books
    ]

    with open(BOOKS_FILE, "w", encoding="utf-8") as file:
        json.dump(books_list, file, ensure_ascii=False, indent=4)


def load_books_from_json():
    """
    Загружает книги из JSON-файла.

    :return: Список книг, загруженных из файла. Если файл не существует или содержит
             некорректные данные, возвращает пустой список.
    """

    if not os.path.exists(BOOKS_FILE):
        return []

    with open(BOOKS_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print("\nОшибка: файл JSON содержит некорректные данные.")
            return []
