FROM node:18

WORKDIR /app

# Instala las dependencias globales necesarias
RUN npm install -g @angular/cli

# Los archivos de configuración primero
COPY package*.json ./
COPY angular.json ./
COPY tsconfig*.json ./
COPY tailwind.config.js ./
COPY postcss.config.js ./

# Instala las dependencias
RUN npm install --legacy-peer-deps

# Copia el resto del código
COPY . .

# Construye los estilos de Tailwind
RUN npx tailwindcss -i src/styles.css -o src/styles.output.css

EXPOSE 4200

# Comando para desarrollo con hot-reload
CMD ["ng", "serve", "--host", "0.0.0.0", "--poll", "2000", "--disable-host-check"]