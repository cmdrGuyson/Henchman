import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", 8000)

app = Flask(__name__)

@app.route("/")
def health():
    return {"status": True}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)