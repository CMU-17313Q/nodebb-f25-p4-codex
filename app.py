from flask import Flask, request, jsonify
import os

from flask import Flask
from flask import request, jsonify
from src.translator import translate

app = Flask(__name__)

@app.route("/", methods=["GET"])
def translator():
    content = request.args.get("content", default = "", type = str)
    is_english, translated_content = translate(content)
    return jsonify({
        "is_english": is_english,
        "translated_content": translated_content,
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)

