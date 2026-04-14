from flask import Flask, render_template, request, redirect , url_for, session
import sqlite3
import os


app = Flask(__name__)
DB_NAME = "books.db"
app.secret_key = "KPLlkjsielkfOIjlkdoeikfiw"

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


@app.route("/")
def home():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    try:
        user = session["user"][1]
    except Exception as e:
        return redirect(url_for("login"))

    return render_template("home.html", user=session["user"][1], books=books)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        usr = conn.execute("SELECT id, username, name, bio, pic_path  FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        conn.close()
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
            print("two passwords must match")
            return redirect(url_for("signup"))

        conn = get_db_connection()
        usr = conn.execute("SELECT username, name, bio, pic_path  FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        conn.execute("INSERT INTO users(id, username, password, name, bio, pic_path) values(?, ?, ?)", (hash(username+password), username, password, "", "", ""))
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
    return render_template("books.html")

@app.route("/profile")
def profile():
    conn = get_db_connection()
    profile = conn.execute("SELECT username, name, pic_path bio FROM users WHERE id = ?", (session["user"][0],)).fetchone()
    curr_books = conn.execute("SELECT * FROM user_books WHERE user_id = ? AND status = ?", (session["user"][0], "reading")).fetchall()
    c_b = []
    for b in curr_books:
        c_b.append(conn.execute("SELECT * FROM books WHERE id = ?", (b["book_id"], )).fetchone())

    read_books = conn.execute("SELECT * FROM user_books WHERE user_id = ? AND status = ?", (session["user"][0], "read")).fetchall()
    plan_books = conn.execute("SELECT * FROM user_books WHERE user_id = ? AND status = ?", (session["user"][0], "plan")).fetchone()
    return render_template("profile.html", profile=profile, no_of_currently_reading=len(c_b), no_of_read=len(read_books), no_of_plan=len(plan_books), current=c_b)

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    conn = get_db_connection()

    if query:
        results = conn.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{query}%", f"%{query}%")).fetchall()
    else:
        results = []
    conn.close()
    print(query)
    print(results)

    return render_template("search.html", no_of_results=len(results), results=results, query=query)


# https://covers.openlibrary.org/b/isbn/9780385533225-S.jpg
if __name__ == "__main__":
    init_db()
    app.run(debug=True)


