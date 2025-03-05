import pymongo
import pandas as pd

# Kết nối MongoDB
MONGO_URI = "mongodb://mongodb:27017"
DB_NAME = "amazon_db"
COLLECTION_RAW = "orders"
COLLECTION_CLEAN = "orders_clean"

mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
raw_collection = db[COLLECTION_RAW]
clean_collection = db[COLLECTION_CLEAN]

# Trích xuất dữ liệu từ MongoDB
data = list(raw_collection.find({}, {"_id": 0}))
df = pd.DataFrame(data)

# Kiểm tra dữ liệu có tồn tại không
if df.empty:
    print("⚠️ No data found in raw collection!")
else:
    # Chuẩn hóa ngày tháng
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], dayfirst=True, errors="coerce")
    df["Order_Time"] = pd.to_datetime(df["Order_Time"], format="%H:%M:%S", errors="coerce")

    # Loại bỏ dòng có lỗi
    df = df.dropna(subset=["Order_Date", "Order_Time"])

    # Xóa dữ liệu cũ trước khi thêm dữ liệu mới (tránh trùng lặp)
    clean_collection.delete_many({})
    
    # Lưu vào MongoDB
    clean_collection.insert_many(df.to_dict("records"))
    print(f"✅ Cleaned data saved to {COLLECTION_CLEAN} with {len(df)} records.")
