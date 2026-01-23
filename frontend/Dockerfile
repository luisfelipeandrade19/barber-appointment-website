FROM node:22-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Expose port
EXPOSE 5173

# Run the application in development mode
# Note: --host is needed to expose the server to the container network
CMD ["npm", "run", "dev", "--", "--host"]
