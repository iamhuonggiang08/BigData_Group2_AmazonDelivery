from kafka import KafkaProducer
import pandas as pd
import json
import time

# Cấu hình Kafka
KAFKA_TOPIC = "amazon_orders"
KAFKA_BROKER = "kafka:9092"

# Cấu hình Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    linger_ms=100,  # Giảm độ trễ gửi batch
    batch_size=16384  # Gửi dữ liệu theo batch
)

# Đọc file CSV theo từng phần nhỏ
chunk_size = 100  # Đọc 100 dòng một lần
file_path = "/app/amazon_delivery.csv"

for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    for _, row in chunk.iterrows():
        message = row.to_dict()
        producer.send(KAFKA_TOPIC, message)
    time.sleep(0.5)  # Tạo khoảng thời gian ngắn giữa các batch gửi

producer.flush()
producer.close()
print("📤 Gửi dữ liệu hoàn tất!")
