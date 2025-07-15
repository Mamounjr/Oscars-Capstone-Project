from flask import Flask, render_template #using flask for building web app
import sqlite3 #sqlite3 for database connection
import os #os for file path management


#Create a Flask app instance
#and set the template and static folders
app = Flask(__name__, template_folder="templates", static_folder="books")

# Function to retrieve books from the database
# Opens library db connection
DB_PATH = os.path.join(os.path.dirname(__file__), "library.db")
def get_books():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        return cursor.fetchall()

#Route that defines url for sports page
@app.route("/sports")
def sports():
    books = get_books()  # Fetch books from the database
    print(books) 
    return render_template("sports_page.html", books=books)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

    