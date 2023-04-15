FROM --platform=linux/amd64  node:lts
WORKDIR /app

COPY package*.json ./
COPY /bundles-src ./bundles-src

RUN npm ci --dev

