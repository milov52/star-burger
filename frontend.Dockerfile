# build env
FROM node:lts
WORKDIR /app

COPY package*.json .
COPY bundles-src/ .

RUN npm ci --dev
CMD ["./node_modules/.bin/parcel watch bundles-src/index.js", "--dist-dir", "bundles", "--public-url='./'"]
