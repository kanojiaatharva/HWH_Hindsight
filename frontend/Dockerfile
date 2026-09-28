FROM node:20-alpine

WORKDIR /app

# Copy package files first for Docker layer caching
COPY package.json package-lock.json ./
RUN npm ci

# Copy application code
COPY . .

# Build the Next.js application
RUN npm run build

# Expose the frontend port
EXPOSE 3000

# Run in production mode
CMD ["npm", "start"]
