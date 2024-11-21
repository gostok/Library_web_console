from database.db import *
from tabulate import tabulate


def add_book_interaction():
    """
    Обрабатывает ввод данных от пользователя для добавления новой книги.
    """

    title = input("Введите название книги: ")
    author = input("Введите имя автора книги: ")
    year = input("Введите год издания книги: ")

    add_book(title, author, year)
    print("\nКнига успешно добавлена.")


def delete_book_interaction():
    """
    Обрабатывает ввод данных от пользователя для удаления книги по ID.
    """

    book_id = input("Введите ID книги, которую хотите удалить: ")

    if delete_book(book_id):
        print("\nКнига успешно удалена.")
    else:
        print("\nОшибка: Книга с таким ID не найдена.")


def search_book_interaction():
    """
    Обрабатывает ввод данных от пользователя для поиска книг.
    """

    search_message = "(можно оставить пустым)"
    title = input(f"Введите название книги {search_message}: ")
    author = input(f"Введите имя автора книги {search_message}: ")
    year = input(f"Введите год издания книги {search_message}: ")

    results = search_book(title, author, year)

    if results:
        print(
            tabulate(
                results, headers=["ID", "Название", "Автор", "Год"], tablefmt="grid"
            )
        )
    else:
        print("\nОшибка: Книги не найдены.")


def display_all_books_interaction():
    """
    Отображает все книги в библиотеке.
    """

    results = display_all_books()

    if results:
        print(
            tabulate(
                results,
                headers=["ID", "Название", "Автор", "Год", "Статус"],
                tablefmt="grid",
            )
        )
    else:
        print("\nОшибка: Нет книг в библиотеке.")


def change_status_book_interaction():
    """
    Обрабатывает ввод данных от пользователя для изменения статуса книги.
    """

    book_id = input("Введите ID книги, статус которой хотите изменить: ")
    new_status = input("Введите новый статус (в наличии/выдана): ").strip().lower()

    if new_status not in ["в наличии", "выдана"]:
        print(
            "\nОшибка: Неверный статус.\nПожалуйста, введите либо 'в наличии', либо 'выдана'."
        )
        return

    if change_status_book(book_id, new_status):
        print("\nСтатус книги успешно обновлён.")
    else:
        print("\nОшибка: Книга с таким ID не найдена.")


def exit_library():
    """
    Завершает работу приложения.
    """

    print("\nВыход из библиотеки")
    exit()
