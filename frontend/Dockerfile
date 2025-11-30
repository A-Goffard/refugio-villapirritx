# ETAPA 1: Construcción (Build)
FROM node:20-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# ETAPA 2: Producción (Nginx)
FROM nginx:stable-alpine as production-stage
# Copiamos los archivos generados por Vue a la carpeta de Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html
# Copiamos nuestra configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]