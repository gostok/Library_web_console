from ui.library_ui import *
from database.db import load_books_from_json, add_book


def main():
    """
    Основная функция приложения, которая инициализирует библиотеку и запускает меню.
    """

    create_library_table()

    print("\nДобро пожаловать в библиотеку.\n")

    books_from_json = load_books_from_json()
    for book in books_from_json:
        add_book(book["title"], book["author"], book["year"])

    while True:
        message_text = (
            "\nМеню:\n"
            "1. Добавить книгу\n"
            "2. Удалить книгу\n"
            "3. Поиск книги\n"
            "4. Отобразить все книги\n"
            "5. Изменить статус книги\n"
            "6. Выйти\n\n"
        )

        print(message_text)

        choice = input("Выберите действие (цифрой) из меню: ")

        if choice == "1":
            add_book_interaction()
        elif choice == "2":
            delete_book_interaction()
        elif choice == "3":
            search_book_interaction()
        elif choice == "4":
            display_all_books_interaction()
        elif choice == "5":
            change_status_book_interaction()
        elif choice == "6":
            exit_library()
        else:
            print(
                "\nОшибка: Что-то пошло не так. Попробуй снова.\nНапоминаю, что выбор нужно сделать цифрой."
            )


if __name__ == "__main__":
    main()
