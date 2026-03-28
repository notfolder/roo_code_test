# ステージ1（buildステージ）: Node.jsでVue.jsアプリをビルドする
FROM node:20-alpine AS build

WORKDIR /app

# 依存ライブラリをインストール
COPY package*.json ./
RUN npm ci

# アプリケーションコードをコピーしてビルドする
COPY . .
RUN npm run build

# ステージ2（productionステージ）: nginxで静的ファイルを配信する
FROM nginx:alpine

# ビルド済み静的ファイルをnginxの公開ディレクトリにコピーする
COPY --from=build /app/dist /usr/share/nginx/html

# nginxの設定ファイルをコピーする
COPY ../nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
