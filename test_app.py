from app import app
from flask import Flask
app = Flask(__name__)

def test_hello():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert response.data == b"Hello, DevSecOps!"