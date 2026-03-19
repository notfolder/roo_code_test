FROM node:18

WORKDIR /app

COPY package*.json tsconfig*.json vite.config.ts index.html ./
COPY src ./src

RUN npm ci

EXPOSE 5173

CMD ["npm","run","dev","--","--host","0.0.0.0","--port","5173"]
