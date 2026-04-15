from flask import Flask, render_template, request, redirect , url_for, session
from dotenv import load_dotenv
import sqlite3
import os


load_dotenv()
app = Flask(__name__)
DB_NAME = "books.db"
app.secret_key = os.getenv("SECRET_KEY")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS books(id INTERGER PRIMARY KEY UNIQUE, 
                   title TEXT, 
                   author TEXT, 
                   file_path TEXT, 
                   page_count INTERGER,
                   isbn TEXT,
                   cover_path TEXT)""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
        """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS book_genres (
        book_id INTEGER,
        genre_id INTEGER,
        PRIMARY KEY (book_id, genre_id),
        FOREIGN KEY (book_id) REFERENCES books(id),
        FOREIGN KEY (genre_id) REFERENCES genres(id)
    )
    """)


    cursor.execute("""CREATE TABLE IF NOT EXISTS user_books(user_id INTERGE, 
                    book_id INTERGER, 
                    progress DECIMAL, 
                    status TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                    FOREIGN KEY (book_id) REFERENCES books(id))""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(id INTERGER UNIQUE, 
                    username TEXT, 
                    name TEXT,
                    bio TEXT,
                    pic_path TEXT,
                    password TEXT)""")
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["POST", "GET"])
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        book_id = request.form.get("book_id")
        conn = get_db_connection()
        conn.execute("INSERT INTO user_books(user_id, book_id, progress, status) values(?, ?, ?, ?)", (session["user"][0], book_id, "N/A", "plan"))
        conn.commit()
        conn.close()

    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()

    return render_template("home.html", user=session["user"][1], books=books)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        usr = conn.execute("SELECT id, username, name, bio, pic_path  FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        conn.close()
        if usr == None:
            return render_template("login.html")
            
        session["user"] = [usr['id'], usr['username'], usr['name'], usr['bio'], usr['pic_path']]
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        repassword = request.form.get("repassword")

        if password != repassword:
            return redirect(url_for("signup"))

        conn = get_db_connection()
        usr = conn.execute("SELECT username, name, bio, pic_path  FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        conn.execute("INSERT INTO users(id, username, password, name, bio, pic_path) values(?, ?, ?, ?, ?, ?)", (hash(username+password), username, password, "", "", ""))
        conn.commit()
        conn.close()
        session["user"] = [hash(username+password), username, "",  "", ""]
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/my_books")
def my_books():
    if "user" not in session:
        return redirect(url_for("login"))
    conn = get_db_connection()
    profile = conn.execute("SELECT username, name, pic_path, bio FROM users WHERE id = ?", (session["user"][0],)).fetchone()
    curr_books = conn.execute("SELECT * FROM user_books WHERE user_id = ? AND status = ?", (session["user"][0], "reading")).fetchall()
    c_b = []
    r_b = []
    p_b = []
    for b in curr_books:
        c_b.append(conn.execute("SELECT * FROM books WHERE id = ?", (b["book_id"], )).fetchone())
    read_books = conn.execute("SELECT * FROM user_books WHERE user_id = ? AND status = ?", (session["user"][0], "read")).fetchall()
    for b in read_books:
        r_b.append(conn.execute("SELECT * FROM books WHERE id = ?", (b["book_id"], )).fetchone())
    plan_books = conn.execute("SELECT * FROM user_books WHERE user_id = ? AND status = ?", (session["user"][0], "plan")).fetchall()
    for b in plan_books:
        p_b.append(conn.execute("SELECT * FROM books WHERE id = ?", (b["book_id"], )).fetchone())
    conn.close()
    return render_template("books.html", current=c_b, plan=p_b, read=r_b)

@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("login"))
    conn = get_db_connection()
    profile = conn.execute("SELECT username, name, pic_path, bio FROM users WHERE id = ?", (session["user"][0],)).fetchone()
    curr_books = conn.execute("SELECT * FROM user_books WHERE user_id = ? AND status = ?", (session["user"][0], "reading")).fetchall()
    c_b = []
    for b in curr_books:
        c_b.append(conn.execute("SELECT * FROM books WHERE id = ?", (b["book_id"], )).fetchone())

    read_books = conn.execute("SELECT * FROM user_books WHERE user_id = ? AND status = ?", (session["user"][0], "read")).fetchall()
    plan_books = conn.execute("SELECT * FROM user_books WHERE user_id = ? AND status = ?", (session["user"][0], "plan")).fetchall()
    conn.close()
    return render_template("profile.html", profile=profile, no_of_currently_reading=len(c_b), no_of_read=len(read_books), no_of_plan=len(plan_books), current=c_b)

@app.route("/search")
def search():
    if "user" not in session:
        return redirect(url_for("login"))
    query = request.args.get("q", "").strip()
    conn = get_db_connection()

    if query:
        results = conn.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{query}%", f"%{query}%")).fetchall()
    else:
        results = []
    conn.close()

    return render_template("search.html", no_of_results=len(results), results=results, query=query)

@app.route("/book/<int:book_id>")
def book_detail(book_id):
    conn = get_db_connection()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if book == None:
        conn.close()
        return "Book not found", 404
    genres = conn.execute("""SELECT genres.name 
                          FROM genres JOIN book_genres ON genres.id = book_genres.genre_id 
                          WHERE book_genres.book_id = ?""", (book_id, )).fetchall()

    conn.close()
    return render_template("book_detail.html", book=book, genres=genres)





# https://covers.openlibrary.org/b/isbn/9780385533225-S.jpg
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
