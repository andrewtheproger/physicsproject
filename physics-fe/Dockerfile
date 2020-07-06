FROM node:lts-alpine

RUN npm install -g http-server
WORKDIR /app
COPY package*.json ./

RUN yarn install

COPY . .

RUN yarn run build --modern

EXPOSE 8080
CMD [ "http-server", "dist" ]
