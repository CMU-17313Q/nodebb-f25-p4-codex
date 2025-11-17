from flask import Flask, request, jsonify
import os
from src.translator import translate_content  # fixed import

app = Flask(__name__)

@app.route("/", methods=["GET"])
def translator():
    content = request.args.get("content", default="", type=str)

    result = translate_content(content)

    return jsonify({
        "isEnglish": result["isEnglish"],
        "translatedContent": result["translatedContent"]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
