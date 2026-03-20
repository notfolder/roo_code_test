# ベースイメージ
FROM python:3.11-slim

# 必要パッケージ
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 依存インストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリコピー（app ディレクトリが /app/app に配置される）
COPY app/ /app/backend/app/

# モジュール探索パスを /app/app に設定
ENV PYTHONPATH=/app

# uvicorn 実行（app.main を指す）
CMD ["uvicorn", "backup.main:app", "--host", "0.0.0.0", "--port", "8000"]
