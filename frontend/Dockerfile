# frontend/Dockerfile
FROM node:25-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

ENV NODE_ENV=production

CMD ["npm", "run", "start"]