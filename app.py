from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    print("Reçu :", data)
    return jsonify({"status": "ok", "message": "Reçu"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
