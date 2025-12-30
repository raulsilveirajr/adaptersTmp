from flask import Flask, jsonify, request

from engine.main_engine import exec_guider

app = Flask(__name__)
port = 80


@app.route("/webhook/accounts", methods=["POST"])
def webhook():
    if request.method == "POST":
        data = request.get_json()
        exec_guider("accounts_json", data)
        # Processar os dados recebidos
        return jsonify(data), 200
    else:
        return jsonify({"error": "Method not allowed"}), 405


if __name__ == "__main__":
    app.run(port=port)
