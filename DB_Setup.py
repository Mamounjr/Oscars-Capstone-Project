import sqlite3

# Connect to the database
connection = sqlite3.connect("library.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    description TEXT,
    image_path TEXT,
    pdf_path TEXT
);
""")

books = [
    ("My Book", "Author 1", "Temp Book 1.", "images/sports-balls.jpg", "pdf/Assignment1.pdf"),
    ("Sports Guide", "Author 2", "Temp Book 2", "images/Play-Sports.jpg", "pdf/Sports-Guide.pdf"), 
]

cursor.execute("SELECT COUNT(*) FROM books")
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO books (title, author, description, image_path, pdf_path) VALUES (?, ?, ?, ?, ?)", books)

connection.commit()
connection.close()

print("Database setup completed successfully!")
