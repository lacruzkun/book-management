from flask import Flask, render_template, request, redirect , url_for, session, send_from_directory
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()
app = Flask(__name__)
DB_NAME = "books.db"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
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
                    email TEXT, 
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
        conn.execute("INSERT INTO user_books(user_id, book_id, progress, status) values(?, ?, ?, ?)", (session["user"]["id"], book_id, "N/A", "plan"))
        conn.commit()
        conn.close()

    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()

    return render_template("home.html", user=session["user"], books=books)

@app.route("/login", methods=["GET", "POST"])
def login():
    init_db()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        hashed = generate_password_hash(password)
        conn = get_db_connection()
        usr = conn.execute("SELECT id, password, username, email, bio, pic_path  FROM users WHERE email = ? ", (email, )).fetchone()

        if not check_password_hash(usr["password"], password):
            print("wrong password")
            return render_template("login.html")

        conn.close()
        print("logging in with ", email, hash(password))
        if usr == None:
            return render_template("login.html")

        user = {
                "id": usr["id"],
                "username": usr["username"],
                "bio": usr["bio"],
                "pic_path": usr["pic_path"],
        }
            
        session["user"] = user
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        repassword = request.form.get("repassword")

        if password != repassword:
            return render_template("signup.html", mismatch=True)
        hashed = generate_password_hash(password)

        conn = get_db_connection()
        conn.execute("""INSERT INTO 
                     users(id, username, password, email, bio, pic_path) 
                     values(?, ?, ?, ?, ?, ?)""", 
                     (hash(username+password), username, hashed,  email, "", ""))
        conn.commit()
        conn.close()
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
    profile = conn.execute("SELECT username,  pic_path, bio FROM users WHERE id = ?", (session["user"]["id"],)).fetchone()
    curr_books = conn.execute("SELECT * FROM user_books WHERE user_id = ? AND status = ?", (session["user"]["id"], "reading")).fetchall()
    c_b = []
    r_b = []
    p_b = []
    for b in curr_books:
        c_b.append(conn.execute("SELECT * FROM books WHERE id = ?", (b["book_id"], )).fetchone())
    read_books = conn.execute("SELECT * FROM user_books WHERE user_id = ? AND status = ?", (session["user"]["id"], "read")).fetchall()
    for b in read_books:
        r_b.append(conn.execute("SELECT * FROM books WHERE id = ?", (b["book_id"], )).fetchone())
    plan_books = conn.execute("SELECT * FROM user_books WHERE user_id = ? AND status = ?", (session["user"]["id"], "plan")).fetchall()
    for b in plan_books:
        p_b.append(conn.execute("SELECT * FROM books WHERE id = ?", (b["book_id"], )).fetchone())
    conn.close()
    return render_template("books.html", current=c_b, plan=p_b, read=r_b)

@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("login"))
    conn = get_db_connection()
    profile = conn.execute("SELECT username, pic_path, bio FROM users WHERE id = ?", (session["user"]["id"],)).fetchone()
    curr_books = conn.execute("SELECT * FROM user_books WHERE user_id = ? AND status = ?", (session["user"]["id"], "reading")).fetchall()
    c_b = []
    for b in curr_books:
        c_b.append(conn.execute("SELECT * FROM books WHERE id = ?", (b["book_id"], )).fetchone())

    read_books = conn.execute("SELECT * FROM user_books WHERE user_id = ? AND status = ?", (session["user"]["id"], "read")).fetchall()
    plan_books = conn.execute("SELECT * FROM user_books WHERE user_id = ? AND status = ?", (session["user"]["id"], "plan")).fetchall()
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

@app.route("/add_profile_pic", methods=["POST", "GET"])
def add_profile_pic():
    file = request.files["file"]
    if file.filename == "":
        return "No file selected"

    filename, ext = (hash("".join(file.filename.split(".")[:-1])), file.filename.split(".")[-1])

    filename = secure_filename(str(filename)) + "." + ext
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    conn = get_db_connection()
    conn.execute("""UPDATE users SET pic_path = ? WHERE id = ?""",
                   (filename, session["user"]["id"]))
    user = {
            "id": session["user"]["id"],
            "username": session["user"]["username"],
            "bio": session["user"]["bio"],
            "pic_path": filename
    }

    session["user"] = user
    conn.commit()
    conn.close()
    return "OK"

@app.route("/<filename>")
def uploaded_file(filename):
    return send_from_directory(
            app.config["UPLOAD_FOLDER"],
            filename
    )





# https://covers.openlibrary.org/b/isbn/9780385533225-S.jpg
if __name__ == "__main__":
    app.run(debug=True)
