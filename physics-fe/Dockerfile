FROM node:lts-alpine as build-stage

WORKDIR /app
COPY package*.json ./

RUN yarn install

COPY . .

RUN yarn run build --https --modern

FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
RUN rm etc/nginx/conf.d/*
RUN mkdir -p /etc/nginx/conf.d/
RUN echo 'server { listen 8080; root /usr/share/nginx/html; }' > /etc/nginx/conf.d/nginx.conf
EXPOSE 8080
CMD [ "nginx", "-g", "daemon off;" ]
