# Estágio de Build
FROM node:20-alpine as build

WORKDIR /app

# Copiar arquivos de dependências
COPY package.json package-lock.json ./

# Instalar dependências
RUN npm ci

# Copiar código fonte
COPY . .

# Buildar a aplicação
RUN npm run build

# Estágio de Produção
FROM nginx:alpine

# Copiar os arquivos buildados do estágio anterior para o diretório padrão do Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Configuração customizada do Nginx para lidar com React Router (SPA)
# Cria um arquivo de configuração inline ou copia um arquivo externo se preferir.
# Aqui vamos sobrescrever o default.conf para garantir que rotas caiam no index.html
RUN echo 'server { \
    listen 80; \
    location / { \
    root /usr/share/nginx/html; \
    index index.html index.htm; \
    try_files $uri $uri/ /index.html; \
    } \
    location /api/ { \
    proxy_pass http://backend:8000; \
    proxy_http_version 1.1; \
    proxy_set_header Upgrade $http_upgrade; \
    proxy_set_header Connection "upgrade"; \
    proxy_set_header Host $host; \
    proxy_cache_bypass $http_upgrade; \
    } \
    }' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
