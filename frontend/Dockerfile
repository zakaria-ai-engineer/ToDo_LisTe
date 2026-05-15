# ── Frontend Dockerfile ─────────────────────────────────────────────────────
# Image de base : Node 20 Alpine (légère)
FROM node:20-alpine

# Dossier de travail
WORKDIR /app

# 1. Copier les manifestes de dépendances en premier (cache Docker)
COPY package.json package-lock.json ./

# 2. Installer les dépendances Node
RUN npm ci

# 3. Copier tout le code source
COPY . .

# Port exposé (Vite dev server)
EXPOSE 5173

# Lancement de Vite en mode dev avec --host pour que Docker expose le port
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
