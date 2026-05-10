from flask import Flask, render_template, request, jsonify
import sys
import os

# Make sure sibling utils/ is importable when running app.py directly
sys.path.insert(0, os.path.dirname(__file__))

from utils.password_checker import check_password
from utils.password_generator import generate_password, generate_passphrase
from utils.crack_time import estimate_crack_time

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")

    result = check_password(password)
    crack_times = estimate_crack_time(result.get("entropy", 0))
    result["crack_times"] = crack_times

    return jsonify(result)


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    mode = data.get("mode", "random")           # "random" | "passphrase"
    length = int(data.get("length", 16))
    use_upper   = data.get("upper",   True)
    use_lower   = data.get("lower",   True)
    use_digits  = data.get("digits",  True)
    use_special = data.get("special", True)

    if mode == "passphrase":
        pw = generate_passphrase(word_count=data.get("words", 4))
    else:
        pw = generate_password(
            length=length,
            use_upper=use_upper,
            use_lower=use_lower,
            use_digits=use_digits,
            use_special=use_special,
        )

    result = check_password(pw)
    crack_times = estimate_crack_time(result.get("entropy", 0))
    result["crack_times"] = crack_times
    result["password"] = pw

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
