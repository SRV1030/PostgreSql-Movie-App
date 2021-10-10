import datetime
import database as db

menu = """Please do the needful
1. Add new movies.
2. View Upcoming movies.
3. View All movies.
4. Watch a movie
5. View watched movies.
6. Create a User.
7. Search for a movie.
8. Exit
"""

db.createTables()


def prompt_add_movie():
    title = input("Enter the title of movie ")
    release_date = input("Release date (dd-mm-YYYY): ")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y").timestamp()  # strp-string parse
    db.inertMovie(title, parsed_date)


def prompt_view_movies(upcoming=False):
    movies = db.getMovies(upcoming=upcoming)
    for _id, title, release_date in movies:
        movie_date = datetime.datetime.fromtimestamp(release_date)
        human_date = movie_date.strftime("%b %d %Y")
        print(f"{_id}: {title} (on {human_date})")
    print("-----------\n")


def prompt_view_watched_movies():
    movies = db.getWatchedMovies(name := input("Enter Watcher Mame: "))
    if movies:
        for movie in movies:
            movie_date = datetime.datetime.fromtimestamp(movie[2])
            human_date = movie_date.strftime("%b %d %Y")
            print(f"{movie[3]}: {movie[1]} (on {human_date})")
    else:
        print("No movies yet\n")
    print("-----------\n")


def prompt_watch_movie():
    db.watchmovie(title := input("Enter user_name "), watcher_name := int(input("Enter movie id: ")))


def prompt_create_user():
    db.insertUser(username := input("Enter the username: "))


def prompt_seatch_movie():
    movies = db.search_movie(title := input("Enter movie string: "))
    if movies:
        for movie in movies:
            movie_date = datetime.datetime.fromtimestamp(movie[2])
            human_date = movie_date.strftime("%b %d %Y")
            print(f"{movie[0]}: {movie[1]} (on {human_date})")
    else:
        print("No movies yet\n")
    print("-----------\n")


while (inp := input(menu)) != "8":
    if inp == "1":
        prompt_add_movie()
    elif inp == "2":
        prompt_view_movies(upcoming=True)
    elif inp == "3":
        prompt_view_movies()
    elif inp == "4":
        prompt_watch_movie()
    elif inp == "5":
        prompt_view_watched_movies()
    elif inp == '6':
        prompt_create_user()
    elif inp == '7':
        prompt_seatch_movie()
    else:
        print("Invalid input")
