import flet as ft
from flet import View, Page, AppBar, ElevatedButton, TextField, Text
from flet import RouteChangeEvent, ViewPopEvent, CrossAxisAlignment, MainAxisAlignment
from pymongo import MongoClient


def main(page: ft.Page) -> None:
    page.title = 'Navigation App'

    client = MongoClient("mongodb://localhost:27017/")  # ⬅️ пишем необходимый локальный адрес
    db = client["mydatabase"]  # ⬅️ указываем наименование базы данных
    collection = db["users"]  # ⬅️ указываем наименование коллекции базы данных


    def add_user(e):
        try:
            name = name_field.value
            surname = surname_field.value
            email = email_field.value
            password = password_field.value
            collection.insert_one({"name": name,
                                   "surname": surname,
                                   "email": email,
                                   "password": password})
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
                    ElevatedButton(text='Go to Navigation', on_click=lambda _: page.go('/add_profile'))
                ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=26
            )
        )

        # Store
        if page.route == '/add_profile':
            page.window_width = 500
            page.window_height = 550
            page.window_resizable = False  # True or False

            page.views.append(
                View(
                    route='/add_profiles',
                    controls=[
                        AppBar(title=Text('Добавление пользователя'), bgcolor='blue'),
                        # Text(value='Добавление пользователя', size=30),
                        # ft.Text("Добавление пользователя", size=20, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            padding=ft.padding.all(16),
                            content=ft.Column([
                                ft.Row([ft.Text("Имя:        "), name_field]),
                                ft.Row([ft.Text("Фамилия:"), surname_field]),
                                ft.Row([ft.Text("E-mail:     "), email_field]),
                                ft.Row([ft.Text("Пароль:   "), password_field]),
                                ft.Row([]),
                                add_button,
                                ElevatedButton(text='Go back',
                                               on_click=lambda _: page.go('/'),
                                               # alignment=MainAxisAlignment.END,  # Расположение кнопки справа
                                               # animate_position=True
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