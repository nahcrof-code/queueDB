import json
import start_file
import os
import atexit
from flask import Flask, jsonify, request


token = start_file.API_TOKEN
DB_FILE = start_file.FILENAME

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    else:
        return {}

def save_db():
    print(f"\nSaving DB to {DB_FILE} before exit...")
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(db, f, indent=4)
        print("Save complete.")
    except Exception as e:
        print(f"Error saving DB: {e}")

db = load_db()

print("Setting startup values...")
startup = start_file.start_rule()
for extra_value in startup:
    db[extra_value] = startup[extra_value]
print("Starting server...")

atexit.register(save_db)

app = Flask(__name__)

def api_error(code: int=500, message: str="Failed request"):
    return jsonify({"message": message, "code": code, "error": True}), code

@app.route("/v1/keys", methods=["GET", "POST", "DELETE"])
def key():
    if request.method == "POST":
        password = request.headers.get("token")
        if password == token:
            post_data = request.json
            try:
                for key_item in post_data:
                    db[key_item] = post_data[key_item]
                return "", 204
            except Exception as e:
                return api_error(code=500, message=str(e))
        else:
            return api_error(code=401, message="invalid token, goober")

    elif request.method == "GET":
        password = request.headers.get("token")
        if password == token:
            keyslist = request.json

            if not keyslist:
                return jsonify(db), 200

            response = {}
            for key_item in keyslist:
                response[key_item] = db.get(key_item)
            return jsonify(response), 200
        else:
            return api_error(code=401, message="invalid token, goober")

    elif request.method == "DELETE":
        password = request.headers.get("token")
        if password == token:
            keyslist = request.json
            try:
                for key_item in keyslist:
                    db.pop(key_item, None)
                return "", 204
            except Exception as e:
                return api_error(code=500, message=str(e))
        else:
            return api_error(code=401, message="invalid token, goober")

if __name__ == "__main__":
    app.run(host=start_file.HOST, port=start_file.PORT)
