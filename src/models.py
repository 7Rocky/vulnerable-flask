from flask_login import UserMixin


class Book:
    def __init__(self, book_id: int, title: str, author: str, cover: str, owner_id: int):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.cover = cover
        self.owner_id = owner_id


class User(UserMixin):
    def __init__(self, user_id: int, username: str, password: str):
        self.user_id = user_id
        self.username = username
        self.password = password

    def get_id(self) -> str:
        return str(self.user_id)
