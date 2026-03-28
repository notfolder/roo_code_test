# ステージ1（buildステージ）: Node.jsでVue.jsアプリをビルドする
# ビルドコンテキストはプロジェクトルート（docker-compose.ymlで設定）
FROM node:20-alpine AS build

WORKDIR /app

# 依存ライブラリをインストール
COPY frontend/package*.json ./
RUN npm install

# アプリケーションコードをコピーしてビルドする
COPY frontend/ .
RUN npm run build

# ステージ2（productionステージ）: nginxで静的ファイルを配信する
FROM nginx:alpine

# ビルド済み静的ファイルをnginxの公開ディレクトリにコピーする
COPY --from=build /app/dist /usr/share/nginx/html

# nginxの設定ファイルをコピーする（ルートコンテキストから参照）
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
