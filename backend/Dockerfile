FROM node:18

WORKDIR /app

COPY package*.json tsconfig.json ./
COPY db ./db
COPY src ./src

RUN npm ci

EXPOSE 3000

CMD ["npm","run","dev"]
