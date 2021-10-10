import datetime
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(os.environ["DATABASE_URL"])

CREATE_TABLE_MOVIES = """CREATE TABLE IF NOT EXISTS movies(
    id SERIAL PRIMARY KEY,
    title TEXT,
    release_date REAL
);"""
# SERIAL IN POSTGRE GIVE AUTO INCREMENTING VALUE

CREATE_TABLE_USER = """CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY
);"""
CREATE_TABLE_WATCHED = """CREATE TABLE IF NOT EXISTS watched(
    user_name TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_name) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);"""

INSERT_MOVIE = "INSERT INTO movies(title,release_date) VALUES (%s,%s);"
INSERT_USER = "INSERT INTO users(username) VALUES (%s);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = %s;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMIN_MOVIES = "SELECT * FROM movies WHERE release_date>%s;"
SELECT_WATCHED_MOVIES = """SELECT movies.*,users.*,watched.movie_id,watched.user_name FROM movies 
JOIN watched ON movies.id=watched.movie_id
JOIN users on users.username=watched.user_name
WHERE watched.user_name=%s
;"""
INSERT_WATCHED_MOVIE = "INSERT INTO watched(user_name,movie_id) VALUES (%s,%s);"
SEARCH_IN_MOVIES = "SELECT * FROM movies WHERE title LIKE %s;"


# CREATE_INDEX="CREATE INDEX IF NOT EXISTS idx_on_release ON movies(release_date);"

def createTables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TABLE_MOVIES)
            cursor.execute(CREATE_TABLE_USER)
            cursor.execute(CREATE_TABLE_WATCHED)


def inertMovie(title, release_date):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIE, (title, release_date))


def insertUser(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username,))


def search_movie(title):
    with connection:
        with connection.cursor() as cursor:
            return cursor.execute(SEARCH_IN_MOVIES, (title,))


def getMovies(upcoming=False):
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                timestamp = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMIN_MOVIES, (timestamp,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)
            return cursor.fetchall()


def watchmovie(watcher_name, movie_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_WATCHED_MOVIE, (watcher_name, movie_id))


def getWatchedMovies(name):
    with connection:
        with connection.cursor() as cursor:
            return cursor.execute(SELECT_WATCHED_MOVIES, (name,))


def deleteMovie(title):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_MOVIE, (title,))
