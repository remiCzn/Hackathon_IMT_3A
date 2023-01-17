FROM node:current-slim
WORKDIR /app
COPY package.json /app
RUN npm install
ADD . /app/
RUN npm run build
CMD ["node", "dist/index.js"]
