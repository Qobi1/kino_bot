import sqlite3
from datetime import date, timedelta
from typing import Optional

connect = sqlite3.connect('moviesdb.db', check_same_thread=False)
cursor = connect.cursor()

try:  # create db
    create_db = """CREATE TABLE "MoviesDatabase" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "title"	TEXT,
                    "video_id"	TEXT NOT NULL UNIQUE,
                    "created_at"	TEXT NOT NULL,
                    "updated_at"	TEXT NOT NULL,
                    "descrption"	TEXT,
                    "thumbnail_url"	TEXT,
                    "genre"  TEXT NULL,
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
                 CREATE TABLE "Users" (
                    "user_id"	INTEGER NOT NULL UNIQUE,
                    "requests"	INTEGER,
                    "is_user"	TEXT,
                    "language"	NUMERIC,
                    "state"	INTEGER,
                    "created_at"	TEXT NOT NULL,
                    "updated_at"	TEXT NOT NULL,
                    PRIMARY KEY("user_id")
                );"""
    connect.execute(create_db)
except sqlite3.OperationalError:  # if db exists
    pass


def get_user(user_id: int = None) -> tuple:
    if user_id:
        user = cursor.execute("Select * from Users where user_id=?", (user_id, )).fetchone()
    else:
        seven_days_ago = date.today() - timedelta(days=7)
        month_ago = date.today() - timedelta(days=30)
        users = cursor.execute("Select * from Users").fetchall()
        total_users = cursor.execute("Select count(*) from Users").fetchall()
        real_users = cursor.execute("Select count(*) from Users where is_user=1").fetchall()
        today_joined = cursor.execute("Select count(*) from Users where created_at=?", (date.today(), )).fetchall()
        joined_this_week = cursor.execute("Select count(*) from Users where created_at>? and created_at<=?", (seven_days_ago, date.today())).fetchall()
        joined_this_month = cursor.execute("Select count(*) from Users where created_at>? and created_at<=?", (month_ago, date.today())).fetchall()
        requests_number = cursor.execute("Select sum(requests) from Users where updated_at=?", (date.today(), )).fetchall()
        user = [users, total_users, real_users, today_joined, joined_this_week, joined_this_month, requests_number]
    return user


def update_user(user_id: int, **values):
    if values.get('language'):
        cursor.execute("Update Users Set updated_at=?, state=?, language=? where user_id=?", (date.today(), 1, values.get('language'), user_id))
    elif values.get('is_user'):
        cursor.execute("Update Users Set updated_at=?, is_user=? where user_id=?", (date.today(), values.get('is_user'), user_id))
    elif values.get('requests'):
        request_number = cursor.execute("Select requests from Users where user_id=?", user_id)
        cursor.execute("Update Users set requests=? where user_id=?", (values.get('requests') + request_number, user_id))
    elif values.get('state'):
        cursor.execute("Update Users Set state=? where user_id=?", (values.get('state'), user_id))
    elif values.get('genre'):
        cursor.execute("Update Users Set genre=? where user_id=?", (values.get('genre'), user_id))
    connect.commit()
    return get_user(user_id)


def create_user(user_id: int) -> None:
    cursor.execute("Insert into Users(user_id, created_at, updated_at) Values(?, ?, ?)", (user_id, date.today(), date.today()))
    connect.commit()


def get_movies() -> list:
    movies = cursor.execute("Select * from MoviesDatabase Order By -id").fetchall()
    # movies = cursor.execute("SELECT * FROM MoviesDatabase ORDER BY id DESC LIMIT 1;").fetchall()
    return movies


def search_movie_by_name(title: str = None):
    movies = cursor.execute(f"""Select * from MoviesDatabase where title like "%{title}%" """).fetchall()
    return movies


def search_movie_by_id(id: int):
    movies = cursor.execute(f"Select video_id from MoviesDatabase where id=?", (id, )).fetchone()
    return movies


def save_movie(user_id: int, movie_id: str) -> None:
    cursor.execute("Insert Into SavedMovies(user_id, movie_id) VALUES(?, ?)", (user_id, movie_id))
    connect.commit()


def search_movie_by_ctg(ctg: str):
    movies = cursor.execute(f"""Select * from MoviesDatabase where genre like "%{ctg}%" """).fetchall()
    return movies
