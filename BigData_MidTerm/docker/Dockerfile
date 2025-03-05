FROM python:3.9

# Cài đặt thư viện cần thiết
RUN pip install kafka-python pymongo pandas

# Tạo thư mục cho ứng dụng
WORKDIR /app

# Sao chép mã nguồn vào container
COPY etl/ /app/

# Chạy lệnh mặc định (có thể ghi đè)
CMD ["python", "kafka_producer.py"]
