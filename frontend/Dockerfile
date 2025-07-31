# frontend/Dockerfile
FROM node:22-slim

WORKDIR /app

COPY package*.json ./
RUN npm update && npm audit fix --force && npm install

COPY . .

RUN npm run build

ENV NODE_ENV=production

CMD ["npm", "run", "start"]