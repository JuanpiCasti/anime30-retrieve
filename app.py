from flask import Flask, jsonify
from scrape import retrieve_animes

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(retrieve_animes())


if __name__ == "__main__":
    app.run()