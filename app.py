from flask import Flask, jsonify, g

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "letterboxd rodando!"})   

if __name__ == '__main__':
    app.run(debug=True)