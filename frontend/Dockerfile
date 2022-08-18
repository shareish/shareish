# dev stage
FROM node:16.13 as dev-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "run", "serve"]

# build stage
FROM dev-stage as build-stage
RUN npm run build

# production stage
# See https://v2.vuejs.org/v2/cookbook/dockerize-vuejs-app.html#Real-World-Example
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
# TODO: copy nginx conf here (and adapt previous line if needed)
COPY configuration.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]