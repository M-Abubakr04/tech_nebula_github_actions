FROM node:18-alpine

# Create app directory
WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy app code
COPY . .

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Change ownership
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 4000

# Run app
CMD ["node", "app.js"]
