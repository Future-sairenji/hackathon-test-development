FROM python:3.11-slim

WORKDIR /app

# ビルドに必要な最小限のパッケージのみインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080

CMD ["python", "main.py"]