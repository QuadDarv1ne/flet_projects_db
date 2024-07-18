import sqlite3
import json
import flet as ft
from flet import View, Page, AppBar, ElevatedButton, TextField, Text
from flet import RouteChangeEvent, ViewPopEvent, CrossAxisAlignment, MainAxisAlignment


def create_database_and_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def save_user(name, surname, email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO users (name, surname, email, password)
        VALUES (?, ?, ?, ?)
    ''', (name, surname, email, password))

    conn.commit()
    conn.close()

create_database_and_table()


def main(page: ft.Page) -> None:
    page.title = 'Navigation App'
    page.theme_mode = ft.ThemeMode.SYSTEM

    def add_user(e):
        try:
            name = name_field.value
            surname = surname_field.value
            email = email_field.value
            password = password_field.value

            save_user(name, surname, email, password)

            page.update()
            page.snack_bar = ft.SnackBar(ft.Text("Данные успешно добавлены"), open=True)
        except Exception as e:
            page.update()
            page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка: {str(e)}"), open=True)

    name_field = ft.TextField(label="Введите имя")
    surname_field = ft.TextField(label="Введите фамилию")
    email_field = ft.TextField(label="Введите e-mail")
    password_field = ft.TextField(label="Введите пароль")
    add_button = ft.ElevatedButton("Добавить", on_click=add_user)

    def route_change(e: RouteChangeEvent) -> None:
        page.views.clear()

        # Home
        page.views.append(
            View(
                route='/',
                controls=[
                    AppBar(title=Text('Home'), bgcolor='blue'),
                    Text(value='Home', size=30),
                    ElevatedButton(text='Регистрация нового пользователя', on_click=lambda _: page.go('/add_profile')),
                    ElevatedButton(text='Авторизация пользователя', on_click=lambda _: page.go('/main_profile'))
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=26
            )
        )

        # Store
        if page.route == '/add_profile':
            page.window_width = 500
            page.window_height = 550
            page.window_resizable = False  # True or False
            page.theme_mode = ft.ThemeMode.SYSTEM

            page.views.append(
                View(
                    route='/add_profiles',
                    controls=[
                        AppBar(title=Text('Добавление пользователя'), bgcolor='blue'),
                        ft.Container(
                            # padding=ft.Padding.all(16),
                            content=ft.Column([
                                ft.Row([ft.Text("Имя:        "), name_field]),
                                ft.Row([ft.Text("Фамилия:"), surname_field]),
                                ft.Row([ft.Text("E-mail:     "), email_field]),
                                ft.Row([ft.Text("Пароль:   "), password_field]),
                                ft.Row([]),
                                add_button,
                                ElevatedButton(text='На главную',
                                               on_click=lambda _: page.go('/'),
                                               )]),
                        ),
                    ],
                ),
            )
        page.update()

        # Store
        if page.route == '/main_profile':
            page.window_width = 500
            page.window_height = 550
            page.window_resizable = False  # True or False
            page.theme_mode = ft.ThemeMode.SYSTEM

            page.views.append(
                View(
                    route='/main_profile',
                    controls=[
                        AppBar(title=Text('Основное меню'), bgcolor='blue'),
                        ft.Container(
                            content=ft.Column([
                                ElevatedButton(text='Выйти',
                                               on_click=lambda _: page.go('/'),
                                               )]),
                        ),
                    ],
                ),
            )
        page.update()

    def view_pop(e: ViewPopEvent) -> None:
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == '__main__':
    ft.app(target=main)

# TODO: Заметки
## Преподаватель: Дуплей Максим Игоревич
## Дата: 18/07/2024