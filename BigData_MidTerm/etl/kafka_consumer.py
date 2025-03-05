from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# Cấu hình Kafka
KAFKA_TOPIC = "amazon_orders"
KAFKA_BROKER = "kafka:9092"

# Cấu hình MongoDB
client = MongoClient("mongodb://mongodb:27017/")
db = client["amazon_db"]
collection = db["orders"]

# Tạo Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    consumer_timeout_ms=10000  # Thời gian chờ nếu không có message
)

batch_size = 50
buffer = []

for message in consumer:
    buffer.append(message.value)
    if len(buffer) >= batch_size:
        collection.insert_many(buffer)  # Ghi vào MongoDB theo batch
        buffer = []

if buffer:
    collection.insert_many(buffer)

consumer.close()
print("📥 Nhận và lưu dữ liệu hoàn tất!")
