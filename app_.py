from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return b"Hello, DevSecOps!"

if __name__ == "__main__":
    app.run()