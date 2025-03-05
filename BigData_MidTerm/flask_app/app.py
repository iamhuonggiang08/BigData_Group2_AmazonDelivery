from flask import Flask, render_template, jsonify
import pymongo
import pandas as pd

app = Flask(__name__)

# Kết nối MongoDB
MONGO_URI = "mongodb://mongodb:27017"
DB_NAME = "amazon_db"
COLLECTION_CLEAN = "orders_clean"

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_CLEAN]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    data = list(collection.find({}, {"_id": 0}))  # Lấy dữ liệu từ MongoDB
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
