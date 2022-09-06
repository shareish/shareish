# dev stage
FROM node:16.13 as dev-stage
WORKDIR /app
COPY package*.json ./
RUN npm config set unsafe-perm true && npm install --force
COPY . .
RUN chown -R node:node /app/node_modules
CMD ["npm", "run", "serve"]

# build stage
FROM dev-stage as build-stage
RUN npm run build

# production stage
# See https://v2.vuejs.org/v2/cookbook/dockerize-vuejs-app.html#Real-World-Example
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY configuration.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]